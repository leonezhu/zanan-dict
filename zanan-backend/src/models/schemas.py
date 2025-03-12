from pydantic import BaseModel
from typing import List, Dict, Union

# 查询请求模型
class QueryRequest(BaseModel):
    """查询请求模型
    
    属性:
        word (str): 要查询的单词
        languages (List[str]): 需要查询的语言列表
        example_count (int): 每种语言生成的示例句子数量，默认为 2
    """
    word: str
    languages: List[str]
    example_count: int = 2

# 定义子模型
class Definition(BaseModel):
    """单词定义模型
    
    属性:
        definition (str): 单词的释义
        phonetic (str): 单词的音标
    """
    definition: str
    phonetic: str

class Example(BaseModel):
    """示例句子模型
    
    属性:
        text (str): 示例句子文本
        audio_url (str): 示例句子的音频URL
    """
    text: str
    audio_url: str = ""

class LanguageResult(BaseModel):
    """单语言查询结果模型
    
    属性:
        definition (Definition): 单词的定义和音标
        examples (List[Example]): 示例句子列表
    """
    definition: Definition
    examples: List[Example]

# 查询响应模型
class QueryResponse(BaseModel):
    """查询响应模型
    
    属性:
        word (str): 查询的单词
        languages (List[str]): 查询的语言列表
        results (Dict): 查询结果，包含 definitions 和 examples 两个子字段
            - definitions (Dict[str, Definition]): 各语言的单词定义
            - examples (Dict[str, List[Example]]): 各语言的示例句子
        timestamp (str): 查询时间，ISO格式的UTC时间字符串
    """
    word: str
    languages: List[str]
    results: Dict[str, Dict[str, Union[Definition, List[Example]]]]
    timestamp: str

# 随机单词请求模型
class RandomWordRequest(BaseModel):
    """随机单词请求模型
    
    属性:
        style (str): 随机单词的风格，如'work'（职场）、'life'（生活）等
        languages (List[str]): 需要查询的语言列表
        example_count (int): 每种语言生成的示例句子数量，默认为 2
    """
    style: str
    languages: List[str]
    example_count: int = 2