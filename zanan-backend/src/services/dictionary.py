from typing import Dict, List, Optional
import json
import os
from datetime import datetime
import asyncio

class DictionaryService:
    """字典服务类
    
    提供单词查询、定义生成和示例句子生成等核心功能。
    当前使用模拟数据，后续可扩展为真实服务。
    """
    
    def __init__(self):
        """初始化字典服务"""
        self.query_dir = "queries/"
        os.makedirs(self.query_dir, exist_ok=True)
    
    async def generate_definition(self, word: str, language: str) -> dict:
        """生成单词定义和音标（模拟数据）
        
        参数:
            word (str): 要查询的单词
            language (str): 目标语言
            
        返回:
            dict: 包含定义和音标的字典
        """
        # 返回模拟数据
        mock_definitions = {
            "en": {"definition": "A greeting or expression of goodwill", "phonetic": "/həˈloʊ/"},
            "zh-yue": {"definition": "打招呼嘅用语", "phonetic": "hēi"},
            "zh": {"definition": "用于打招呼的用语", "phonetic": "nǐ hǎo"},
            "zh-sc": {"definition": "问候语，打招呼的话", "phonetic": "nī hǎo"}
        }
        return mock_definitions.get(language.lower(), {"definition": f"Mock definition for {word}", "phonetic": ""})
    
    async def generate_example(self, word: str, language: str) -> str:
        """生成示例句子（模拟数据）
        
        参数:
            word (str): 要使用的单词
            language (str): 目标语言
            
        返回:
            str: 示例句子
        """
        # 返回模拟数据
        mock_examples = {
            "en": f"Hello, how are you today?",
            "zh-yue": f"喂，你今日点啊？",
            "zh": f"你好，今天怎么样？",
            "zh-sc": f"倷好，今朝个咋样？"
        }
        return mock_examples.get(language.lower(), f"Mock example sentence for {word}")
    
    async def query_word(self, word: str, languages: List[str]) -> Dict:
        """查询单词信息
        
        为指定单词生成多语言的定义、音标和示例句子。
        
        参数:
            word (str): 要查询的单词
            languages (List[str]): 目标语言列表
            
        返回:
            Dict: 包含所有语言查询结果的字典
        """
        # 并行处理每种语言的查询
        definition_tasks = [self.generate_definition(word, lang) for lang in languages]
        example_tasks = [self.generate_example(word, lang) for lang in languages]
        
        # 等待所有异步任务完成
        definitions_list = await asyncio.gather(*definition_tasks)
        examples_list = await asyncio.gather(*example_tasks)
        
        # 整理结果
        definitions = {lang: def_dict for lang, def_dict in zip(languages, definitions_list)}
        examples = {lang: example for lang, example in zip(languages, examples_list)}
        
        result = {
            "definitions": definitions,
            "examples": examples
        }
        
        # 保存查询记录
        await self.save_query_record(word, languages, result)
        
        return result
    
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