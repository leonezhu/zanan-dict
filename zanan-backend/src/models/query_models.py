from typing import List, Dict, Optional
from pydantic import BaseModel

class Definition(BaseModel):
    """词汇定义模型"""
    definition: str
    phonetic: str
    audio_url: Optional[str] = ""

class Example(BaseModel):
    """示例句子模型"""
    text: str
    audio_url: Optional[str] = ""

class LanguageResult(BaseModel):
    """单一语言的查询结果"""
    definition: Definition
    examples: List[Example]

class QueryRequest(BaseModel):
    """查询请求模型"""
    word: str
    languages: List[str]
    example_count: int = 2

class QueryResponse(BaseModel):
    """查询响应模型"""
    word: str
    languages: List[str]
    results: Dict[str, LanguageResult]
    timestamp: str