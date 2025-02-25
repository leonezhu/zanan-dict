from typing import Dict, List, Optional, Protocol
import json
import os
from datetime import datetime
import asyncio
from abc import ABC, abstractmethod
from .tts.edge_tts_generator import EdgeTTSGenerator
from .tts.dui_tts_generator import DuiTTSGenerator
from ..utils.audio_base import AudioGeneratorStrategy
from ..config import STORAGE_DIR

class LanguageStrategy(Protocol):
    """语言策略接口
    
    定义了不同语言实现类需要实现的方法。
    """
    def __init__(self):
        """初始化语言策略
        """
        self.language_code = "zh"  # 默认语言代码
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """获取音频生成器
        
        返回:
            AudioGeneratorStrategy: 音频生成器实例
        """
        raise NotImplementedError
    
    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标"""
        ...
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到目标语言"""
        ...
        
    async def generate_audio(self, text: str, word: str) -> Optional[str]:
        """生成音频文件
        
        将给定文本转换为语音，并保存为音频文件。
        
        参数:
            text (str): 要转换的文本内容
            word (str): 相关单词，用于生成文件名
            
        返回:
            Optional[str]: 成功时返回音频文件的URL路径，失败时返回 None
        """
        return await self.tts_generator.generate_audio(text, self.language_code, word)

class DictionaryService:
    """字典服务类
    
    提供单词查询、定义生成和示例句子生成等核心功能。
    使用策略模式支持不同语言的实现。
    """
    
    def __init__(self):
        """初始化字典服务"""
        self.storage_dir = STORAGE_DIR
        self.query_dir = os.path.join(self.storage_dir, "queries")
        os.makedirs(self.query_dir, exist_ok=True)
        
        # 初始化语言策略映射
        self.language_strategies = {
            "en": EnglishStrategy(),
            "zh-yue": CantoneseStrategy(),
            "zh": MandarinStrategy(),
            "zh-sc": SichuaneseStrategy()
        }
        
        # 初始化 LLM 服务
        from .llms.llm_service import LLMService
        self.llm_service = LLMService()
        
        # 默认英文例句模板
        self.default_examples = [
            "The word {word} is useful.",
            "I like the word {word}."
        ]
    
    def get_strategy(self, language: str) -> LanguageStrategy:
        """获取语言对应的策略实现
        
        参数:
            language (str): 目标语言
            
        返回:
            LanguageStrategy: 对应语言的策略实现
        """
        return self.language_strategies.get(language.lower(), self.language_strategies["en"])
    
    async def generate_definition(self, word: str, language: str) -> dict:
        """生成单词定义和音标
        
        参数:
            word (str): 要查询的单词
            language (str): 目标语言
            
        返回:
            dict: 包含定义和音标的字典
        """
        strategy = self.get_strategy(language)
        return await strategy.generate_definition(word)
    
    async def generate_base_examples(self, word: str, count: int = 5) -> List[str]:
        """生成基础英文例句
        
        参数:
            word (str): 要使用的单词
            count (int): 需要生成的例句数量
            
        返回:
            List[str]: 生成的英文例句列表
        """
        try:
            # 调用 LLM 服务生成例句
            response = await self.llm_service.generate_examples(word, count)
            if response and isinstance(response, list):
                # 直接使用返回的例句列表
                return response[:count]
            
        except Exception as e:
            print(f"LLM 服务调用错误: {e}")
        
        # 发生错误时返回基础示例
        return [example.format(word=word) for example in self.default_examples][:count]
    
    async def generate_examples(self, word: str, language: str, count: int = 5) -> List[str]:
        """生成示例句子列表
        
        参数:
            word (str): 要使用的单词
            language (str): 目标语言
            count (int): 需要生成的例句数量
            
        返回:
            List[str]: 示例句子列表
        """
        # 首先生成基础英文例句
        base_examples = await self.generate_base_examples(word, count)
        print(f" base_examples: {base_examples}")
        
        # 如果目标语言是英语，直接返回基础例句
        if language.lower() == "en":
            return base_examples
            
        # 对于其他语言，翻译成目标语言
        strategy = self.get_strategy(language)
        return await strategy.translate_examples(base_examples)
    
    async def query_word(self, word: str, languages: List[str], example_count: int = 2) -> Dict:
        # 首先生成基础英文例句
        base_examples = await self.generate_base_examples(word, example_count)
        print(f"Base examples generated: {base_examples}")
        
        # 并行处理每种语言的查询
        definition_tasks = [self.generate_definition(word, lang) for lang in languages]
        example_tasks = []
        audio_tasks = []
        
        # 根据语言生成翻译任务
        for lang in languages:
            if lang.lower() == "en":
                # 英语直接使用基础例句
                example_tasks.append(asyncio.create_task(asyncio.sleep(0, base_examples)))
            else:
                # 其他语言需要翻译
                strategy = self.get_strategy(lang)
                example_tasks.append(strategy.translate_examples(base_examples))
        
        # 等待所有异步任务完成
        definitions_list = await asyncio.gather(*definition_tasks)
        examples_list = await asyncio.gather(*example_tasks)
        
        # 整理结果 - 按照语言分组
        results = {
            'definitions': {},
            'examples': {}
        }
        
        # 处理定义
        for lang, def_dict in zip(languages, definitions_list):
            results['definitions'][lang] = def_dict
        
        # 处理示例并生成音频URL
        for lang, example_list in zip(languages, examples_list):
            lang_examples = []
            strategy = self.get_strategy(lang)
            for example in example_list:
                # 创建音频生成任务
                audio_task = strategy.generate_audio(example, word)
                audio_tasks.append(audio_task)
                lang_examples.append({
                    'text': example,
                    'audio_url': ""
                })
            results['examples'][lang] = lang_examples
        
        # 等待所有音频生成任务完成
        audio_urls = await asyncio.gather(*audio_tasks)
        
        # 更新音频URL
        audio_index = 0
        for lang_examples in results['examples'].values():
            for example in lang_examples:
                audio_url = audio_urls[audio_index] or ""
                example['audio_url'] = audio_url
                audio_index += 1
        
        # 创建完整的响应数据
        response_data = {
            'word': word,
            'languages': languages,
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # 所有音频生成完成后，保存查询记录
        await self.save_query_record(word, languages, results)
        
        # 返回完整的响应数据
        return response_data
        
        # 返回与保存格式一致的数据结构
        return {
            'word': word,
            'languages': languages,
            'results': results,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def save_query_record(self, word: str, languages: List[str], results: Dict):
        """保存查询记录
        
        将查询结果保存到本地 JSON 文件中。
        
        参数:
            word (str): 查询的单词
            languages (List[str]): 查询的语言列表
            results (Dict): 查询结果
        """
        record = {
            "word": word,
            "languages": languages,
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        filename = os.path.join(self.query_dir, f"{word}_{datetime.utcnow().timestamp()}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=4)

class EnglishStrategy(LanguageStrategy):
    """英语策略实现类"""
    def __init__(self):
        """初始化英语策略"""
        super().__init__()
        from .llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "en"
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """获取音频生成器
        
        返回:
            AudioGeneratorStrategy: 音频生成器实例
        """
        from .tts.edge_tts_generator import EdgeTTSGenerator
        return EdgeTTSGenerator()

    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标
        
        使用 LLM 服务生成英语定义和音标。
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义和音标的字典
        """
        try:
            prompt = f"Please provide the definition and phonetic transcription for the word '{word}' in English. Format your response as follows:\nDefinition: [clear and concise definition]\nPhonetic: [IPA phonetic transcription]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # 解析响应文本
                lines = response.strip().split('\n')
                definition = ""
                phonetic = ""
                
                for line in lines:
                    if line.startswith("Definition:"):
                        definition = line.replace("Definition:", "").strip()
                    elif line.startswith("Phonetic:"):
                        phonetic = line.replace("Phonetic:", "").strip()
                
                return {"definition": definition, "phonetic": phonetic}
                
        except Exception as e:
            print(f"[EnglishStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子"""
        """英语不用实现这个方法，因为生成的模板例句就是英语的 """
        # print(f"[EnglishStrategy] 未实现 translate_examples 方法，例句数量: {len(examples)}")
        return examples

class CantoneseStrategy(LanguageStrategy):
    """粤语策略实现类"""
    def __init__(self):
        """初始化粤语策略"""
        super().__init__()
        from .llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "zh-yue"
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """获取音频生成器
        
        返回:
            AudioGeneratorStrategy: 音频生成器实例
        """
        from .tts.edge_tts_generator import EdgeTTSGenerator
        return EdgeTTSGenerator()

    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标
        
        使用 LLM 服务生成粤语定义和音标。
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义和音标的字典
        """
        try:
            prompt = f"请提供单词 '{word}' 的广东话（粤语）解释和粤语拼音。要求：\n1. 使用繁体字\n2. 解释要简洁易懂\n3. 使用粤语发音系统（粤拼）注音\n4. 按以下格式回复：\n解释：[广东话解释]\n粤拼：[粤语拼音]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # 解析响应文本
                lines = response.strip().split('\n')
                definition = ""
                phonetic = ""
                
                for line in lines:
                    if line.startswith("解释："):
                        definition = line.replace("解释：", "").strip()
                    elif line.startswith("粤拼："):
                        phonetic = line.replace("粤拼：", "").strip()
                
                return {"definition": definition, "phonetic": phonetic}
                
        except Exception as e:
            print(f"[CantoneseStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到粤语
        
        使用 LLM 服务将英语例句翻译成粤语。
        
        参数:
            examples (List[str]): 要翻译的英语例句列表
            
        返回:
            List[str]: 翻译后的粤语例句列表
        """
        translated = []
        for example in examples:
            try:
                # 使用 LLM 服务翻译
                prompt = f"请将以下英语句子翻译成地道的广东粤语（使用繁体字）。要求：\n1. 使用日常对话中常见的粤语表达方式\n2. 确保符合粤语的语法结构和表达习惯\n3. 翻译要自然流畅，避免生硬的直译\n4.只返回翻译后的句子，不要添加任何其他说明\n5.翻译的句子中不要出现字母和符号，只包含粤语\n句子：{example}"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                print(f" response: {response}")
                if response and isinstance(response, str):
                    translated.append(response)
                else:
                    print(f"[CantoneseStrategy] LLM 服务返回无效结果，例句: {example}")
                    translated.append(example)
                    
            except Exception as e:
                print(f"[CantoneseStrategy] 翻译错误: {e}, 例句: {example}")
                translated.append(example)
                
        return translated

class MandarinStrategy(LanguageStrategy):
    """普通话策略实现类"""
    def __init__(self):
        """初始化普通话策略"""
        super().__init__()
        from .llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "zh"
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """获取音频生成器
        
        返回:
            AudioGeneratorStrategy: 音频生成器实例
        """
        from .tts.dui_tts_generator import DuiTTSGenerator
        return DuiTTSGenerator()

    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标
        
        使用 LLM 服务生成普通话定义和音标。
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义和音标的字典
        """
        try:
            prompt = f"请提供词语 '{word}' 的中文（普通话）解释和拼音。要求：\n1. 使用简体字\n2. 解释要简洁易懂\n3. 使用汉语拼音注音（包含声调）\n4. 按以下格式回复：\n解释：[中文解释]\n拼音：[汉语拼音]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # 解析响应文本
                lines = response.strip().split('\n')
                definition = ""
                phonetic = ""
                
                for line in lines:
                    if line.startswith("解释："):
                        definition = line.replace("解释：", "").strip()
                    elif line.startswith("拼音："):
                        phonetic = line.replace("拼音：", "").strip()
                
                return {"definition": definition, "phonetic": phonetic}
                
        except Exception as e:
            print(f"[MandarinStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到普通话
        
        使用 LLM 服务将英语例句翻译成普通话。
        
        参数:
            examples (List[str]): 要翻译的英语例句列表
            
        返回:
            List[str]: 翻译后的普通话例句列表
        """
        translated = []
        for example in examples:
            try:
                # 使用 LLM 服务翻译
                prompt = f"请将以下英语句子翻译成地道的普通话（使用简体字）。要求：\n1. 使用日常对话中常见的表达方式\n2. 确保符合普通话的语法结构和表达习惯\n3. 翻译要自然流畅，避免生硬的直译\n4. 只返回翻译后的句子，不要添加任何其他说明\n5. 翻译的句子中不要出现字母和符号，只包含中文\n句子：{example}"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                print(f" response: {response}")
                if response and isinstance(response, str):
                    translated.append(response)
                else:
                    print(f"[MandarinStrategy] LLM 服务返回无效结果，例句: {example}")
                    translated.append(example)
                    
            except Exception as e:
                print(f"[MandarinStrategy] 翻译错误: {e}, 例句: {example}")
                translated.append(example)
                
        return translated

class SichuaneseStrategy(LanguageStrategy):
    """四川话策略实现类"""
    def __init__(self):
        """初始化四川话策略"""
        super().__init__()
        from .llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "zh-sc"
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """获取音频生成器
        
        返回:
            AudioGeneratorStrategy: 音频生成器实例
        """
        from .tts.dui_tts_generator import DuiTTSGenerator
        return DuiTTSGenerator()

    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标
        
        使用 LLM 服务生成四川话定义和音标。
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义和音标的字典
        """
        try:
            prompt = f"请提供词语 '{word}' 的四川话解释和注音。要求：\n1. 使用简体字\n2. 解释要简洁易懂，使用地道的四川话表达\n3. 使用四川话拼音注音（参考汉语拼音，标注声调）\n4. 按以下格式回复：\n解释：[四川话解释]\n音标：[四川话拼音]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # 解析响应文本
                lines = response.strip().split('\n')
                definition = ""
                phonetic = ""
                
                for line in lines:
                    if line.startswith("解释："):
                        definition = line.replace("解释：", "").strip()
                    elif line.startswith("音标："):
                        phonetic = line.replace("音标：", "").strip()
                
                return {"definition": definition, "phonetic": phonetic}
                
        except Exception as e:
            print(f"[SichuaneseStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到四川话
        
        使用 LLM 服务将英语例句翻译成四川话。
        
        参数:
            examples (List[str]): 要翻译的英语例句列表
            
        返回:
            List[str]: 翻译后的四川话例句列表
        """
        translated = []
        for example in examples:
            try:
                # 使用 LLM 服务翻译
                prompt = f"请将以下英语句子翻译成四川话（使用简体字），不需要解释：\n{example}"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                print(f" response: {response}")
                if response and isinstance(response, str):
                    translated.append(response)
                else:
                    print(f"[SichuaneseStrategy] LLM 服务返回无效结果，例句: {example}")
                    translated.append(example)
                    
            except Exception as e:
                print(f"[SichuaneseStrategy] 翻译错误: {e}, 例句: {example}")
                translated.append(example)
                
        return translated