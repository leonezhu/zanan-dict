from typing import Dict, List, Optional, Protocol
import json
import os
from datetime import datetime
import asyncio
from abc import ABC, abstractmethod
from ..utils.audio import AudioGenerator

class LanguageStrategy(Protocol):
    """语言策略接口
    
    定义了不同语言实现类需要实现的方法。
    """
    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标"""
        ...
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到目标语言"""
        ...

class DictionaryService:
    """字典服务类
    
    提供单词查询、定义生成和示例句子生成等核心功能。
    使用策略模式支持不同语言的实现。
    """
    
    def __init__(self):
        """初始化字典服务"""
        self.query_dir = "queries/"
        os.makedirs(self.query_dir, exist_ok=True)
        
        # 初始化语言策略映射
        self.language_strategies = {
            "en": EnglishStrategy(),
            "zh-yue": CantoneseStrategy(),
            "zh": MandarinStrategy(),
            "zh-sc": SichuaneseStrategy()
        }
        
        # 初始化例句生成服务
        self.example_service = ExampleGenerationService()
        
        # 初始化音频生成器
        self.audio_generator = AudioGenerator("storage")
    
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
        """生成基础示例句子列表
        
        参数:
            word (str): 要使用的单词
            count (int): 需要生成的例句数量
            
        返回:
            List[str]: 英文基础示例句子列表
        """
        return await self.example_service.generate_examples(word, count)
    
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
        audio_tasks = []
        for lang, example_list in zip(languages, examples_list):
            lang_examples = []
            for example in example_list:
                # 创建音频生成任务
                audio_task = self.audio_generator.generate_audio(example, lang, word)
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

class ExampleGenerationService:
    """示例句子生成服务
    
    负责调用 LLM 服务生成英文基础例句。
    其他语言仍使用模拟数据。
    """
    def __init__(self):
        """初始化示例句子生成服务"""
        from .llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.default_examples = [
            "The word {word} is useful.",
            "I like the word {word}."
        ]
    
    async def generate_examples(self, word: str, count: int = 5) -> List[str]:
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

class MockLanguageStrategy:
    """模拟数据的语言策略基类"""
    def __init__(self, definitions: dict, translated_examples: Dict[str, str]):
        self.definitions = definitions
        self.translated_examples = translated_examples
    
    async def generate_definition(self, word: str) -> dict:
        return self.definitions
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        # 对于每个例句，如果在预定义翻译中找不到，则生成一个基于模板的翻译
        translated = []
        for example in examples:
            if example in self.translated_examples:
                translated.append(self.translated_examples[example])
            else:
                # 如果没有预定义翻译，使用一个基本的翻译模板
                translated.append(f"喂，{example}")
        return translated

class EnglishStrategy(MockLanguageStrategy):
    """英语策略实现类"""
    def __init__(self):
        super().__init__(
            {"definition": "A greeting or expression of goodwill", "phonetic": "/həˈloʊ/"},
            {
                "How are you today?": "Hello, how are you today?",
                "Nice to meet you!": "Hello, nice to meet you!",
                "Welcome to our meeting.": "Hello, everyone! Welcome to our meeting.",
                "What's the weather like?": "Hello! What's the weather like today?",
                "Can you help me?": "Hello! Can you help me with something?"
            }
        )

class CantoneseStrategy:
    """粤语策略实现类"""
    def __init__(self):
        """初始化粤语策略"""
        from .llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.default_definition = {"definition": "打招呼嘅用语", "phonetic": "hēi"}
        self.default_translations = {
            "How are you today?": "喂，你今日点啊？",
            "Nice to meet you!": "喂，好开心见到你！",
            "Welcome to our meeting.": "喂，大家好！欢迎来开会。",
            "What's the weather like?": "喂，今日天气点啊？",
            "Can you help me?": "喂，你可唔可以帮下我？"
        }
    
    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标"""
        return self.default_definition
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到粤语
        
        使用 LLM 服务将英语例句翻译成粤语。如果 LLM 服务调用失败，
        则返回预定义的翻译或基础模板翻译。
        
        参数:
            examples (List[str]): 要翻译的英语例句列表
            
        返回:
            List[str]: 翻译后的粤语例句列表
        """
        translated = []
        for example in examples:
            try:
                # 首先检查是否有预定义翻译
                if example in self.default_translations:
                    translated.append(self.default_translations[example])
                    continue
                    
                # 使用 LLM 服务翻译
                prompt = f"请将以下英语句子翻译成地道的广东粤语（使用繁体字）。要求：\n1. 使用日常对话中常见的粤语表达方式\n2. 确保符合粤语的语法结构和表达习惯\n3. 翻译要自然流畅，避免生硬的直译\n4.只返回翻译后的句子，不要添加任何其他说明\n5.翻译的句子中不要出现字母和符号，只包含粤语\n句子：{example}"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                print(f" response: {response}")
                if response and isinstance(response, str):
                    translated.append(response)
                else:
                    # 如果 LLM 返回无效结果，使用基础模板
                    translated.append(f"喂，{example}")
                    
            except Exception as e:
                print(f"粤语翻译错误: {e}")
                # 发生错误时使用基础模板
                translated.append(f"喂，{example}")
                
        return translated

class MandarinStrategy(MockLanguageStrategy):
    """普通话策略实现类"""
    def __init__(self):
        super().__init__(
            {"definition": "用于打招呼的用语", "phonetic": "nǐ hǎo"},
            {
                "How are you today?": "你好，今天怎么样？",
                "Nice to meet you!": "你好，很高兴见到你！",
                "Welcome to our meeting.": "大家好！欢迎参加我们的会议。",
                "What's the weather like?": "你好，今天天气怎么样？",
                "Can you help me?": "你好，能帮我一下吗？"
            }
        )

class SichuaneseStrategy:
    """四川话策略实现类"""
    def __init__(self):
        """初始化四川话策略"""
        from .llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.default_definition = {"definition": "问候语，打招呼的话", "phonetic": "nī hǎo"}
        self.default_translations = {
            "How are you today?": "倷好，今朝个咋样？",
            "Nice to meet you!": "倷好，欢喜见到你哦！",
            "Welcome to our meeting.": "大家好！欢迎参加我们个会。",
            "What's the weather like?": "倷好，今朝个天气咋样？",
            "Can you help me?": "倷好，帮我个忙嘛？"
        }
    
    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标"""
        return self.default_definition
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到四川话
        
        使用 LLM 服务将英语例句翻译成四川话。如果 LLM 服务调用失败，
        则返回预定义的翻译或基础模板翻译。
        
        参数:
            examples (List[str]): 要翻译的英语例句列表
            
        返回:
            List[str]: 翻译后的四川话例句列表
        """
        translated = []
        for example in examples:
            try:
                # 首先检查是否有预定义翻译
                if example in self.default_translations:
                    translated.append(self.default_translations[example])
                    continue
                    
                # 使用 LLM 服务翻译
                prompt = f"请将以下英语句子翻译成四川话（使用简体字），不需要解释：\n{example}"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                print(f" response: {response}")
                if response and isinstance(response, str):
                    translated.append(response)
                else:
                    # 如果 LLM 返回无效结果，使用基础模板
                    translated.append(f"倷好，{example}")
                    
            except Exception as e:
                print(f"四川话翻译错误: {e}")
                # 发生错误时使用基础模板
                translated.append(f"倷好，{example}")
                
        return translated