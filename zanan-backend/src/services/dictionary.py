from typing import Dict, List, Optional, Protocol
import json
import os
from datetime import datetime
import asyncio
from abc import ABC, abstractmethod
from ..utils.audio import MockAudioGenerator as AudioGenerator

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
        # 然后翻译成目标语言
        strategy = self.get_strategy(language)
        return await strategy.translate_examples(base_examples)
    
    async def query_word(self, word: str, languages: List[str], example_count: int = 2) -> Dict:
        # 并行处理每种语言的查询
        definition_tasks = [self.generate_definition(word, lang) for lang in languages]
        example_tasks = [self.generate_examples(word, lang, example_count) for lang in languages]
        
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
            for example in example_list:
                audio_url = self.audio_generator.generate_audio(example, lang, word)
                lang_examples.append({
                    'text': example,
                    'audio_url': audio_url or ""
                })
            results['examples'][lang] = lang_examples
        
        # 保存查询记录
        await self.save_query_record(word, languages, results)
        
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
    
    负责调用外部服务 API 生成英文基础例句。
    实际项目中需要替换为真实的服务调用。
    """
    async def generate_examples(self, word: str, count: int = 5) -> List[str]:
        """生成基础英文例句
        
        参数:
            word (str): 要使用的单词
            count (int): 需要生成的例句数量
            
        返回:
            List[str]: 生成的英文例句列表
        """
        # TODO: 实现实际的服务调用
        # 这里使用模拟数据作为示例
        return [
            f"How are you using {word} today?",
            f"Nice to learn the word {word}!",
            f"Welcome to our {word} meeting.",
            f"What's the {word} like?",
            f"Can you help me with {word}?"
        ][:count]

class MockLanguageStrategy:
    """模拟数据的语言策略基类"""
    def __init__(self, definitions: dict, translated_examples: Dict[str, str]):
        self.definitions = definitions
        self.translated_examples = translated_examples
    
    async def generate_definition(self, word: str) -> dict:
        return self.definitions
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        return [self.translated_examples.get(example, example) for example in examples]

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

class CantoneseStrategy(MockLanguageStrategy):
    """粤语策略实现类"""
    def __init__(self):
        super().__init__(
            {"definition": "打招呼嘅用语", "phonetic": "hēi"},
            {
                "How are you today?": "喂，你今日点啊？",
                "Nice to meet you!": "喂，好开心见到你！",
                "Welcome to our meeting.": "喂，大家好！欢迎来开会。",
                "What's the weather like?": "喂，今日天气点啊？",
                "Can you help me?": "喂，你可唔可以帮下我？"
            }
        )

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

class SichuaneseStrategy(MockLanguageStrategy):
    """四川话策略实现类"""
    def __init__(self):
        super().__init__(
            {"definition": "问候语，打招呼的话", "phonetic": "nī hǎo"},
            {
                "How are you today?": "倷好，今朝个咋样？",
                "Nice to meet you!": "倷好，欢喜见到你哦！",
                "Welcome to our meeting.": "大家好！欢迎参加我们个会。",
                "What's the weather like?": "倷好，今朝个天气咋样？",
                "Can you help me?": "倷好，帮我个忙嘛？"
            }
        )