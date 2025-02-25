from typing import Dict, List
import json
import os
from datetime import datetime
import asyncio

from .strategies.english import EnglishStrategy
from .strategies.cantonese import CantoneseStrategy
from .strategies.mandarin import MandarinStrategy
from .strategies.sichuan import SichuaneseStrategy
from .strategies.language_strategy import LanguageStrategy
from ..config import STORAGE_DIR

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
        
        # 如果目标语言是英语，直接返回基础例句
        if language.lower() == "en":
            return base_examples
            
        # 对于其他语言，翻译成目标语言
        strategy = self.get_strategy(language)
        return await strategy.translate_examples(base_examples)
    
    async def query_word(self, word: str, languages: List[str], example_count: int = 2) -> Dict:
        # 首先生成基础英文例句
        base_examples = await self.generate_base_examples(word, example_count)
        
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