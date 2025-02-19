from pydantic import BaseModel
from typing import List, Dict

# 查询请求模型
class QueryRequest(BaseModel):
    """查询请求模型
    
    属性:
        word (str): 要查询的单词
        languages (List[str]): 需要查询的语言列表
    """
    word: str
    languages: List[str]

# 查询响应模型
class QueryResponse(BaseModel):
    """查询响应模型
    
    属性:
        definitions (Dict[str, dict]): 各语言的单词定义和音标
            格式: {"语言": {"definition": "定义", "phonetic": "音标"}}
        examples (Dict[str, str]): 各语言的示例句子
            格式: {"语言": "示例句子"}
        audio_urls (Dict[str, str]): 各语言的音频文件URL
            格式: {"语言": "音频URL"}
    """
    definitions: Dict[str, dict]
    examples: Dict[str, str]
    audio_urls: Dict[str, str]