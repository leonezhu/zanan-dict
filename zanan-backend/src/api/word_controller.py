from fastapi import APIRouter, HTTPException
from typing import List
import os
import json
from datetime import datetime

from ..models.schemas import QueryRequest, QueryResponse
from ..services.dictionary import DictionaryService

router = APIRouter()
dictionary_service = DictionaryService()

@router.post("/api/query", response_model=QueryResponse)
async def query_word(request: QueryRequest):
    """查询单词接口
    
    接收前端的查询请求，返回多语言的单词释义、示例句子和音频URL。
    
    参数:
        request (QueryRequest): 查询请求，包含要查询的单词和目标语言列表
        
    返回:
        QueryResponse: 查询结果，包含各语言的释义、示例句子和音频URL
        
    异常:
        HTTPException: 当查询失败时抛出异常
    """
    try:
        # 参数验证
        if not request.word:
            raise HTTPException(status_code=400, detail="单词不能为空")
        if not request.languages:
            raise HTTPException(status_code=400, detail="至少需要指定一种目标语言")
            
        # 调用服务层处理查询
        result = await dictionary_service.query_word(request.word, request.languages)
        
        # 构造响应
        response = QueryResponse(
            definitions=result["definitions"],
            examples=result["examples"],
            audio_urls={lang: "" for lang in request.languages}  # 暂时返回空URL，后续实现TTS功能
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/queries")
async def get_query_history():
    """获取查询历史记录
    
    返回所有历史查询记录。
    
    返回:
        dict: 包含查询记录列表的字典
    
    异常:
        HTTPException: 当获取记录失败时抛出异常
    """
    try:
        query_dir = dictionary_service.query_dir
        if not os.path.exists(query_dir):
            return {"queries": []}
        
        queries = []
        for filename in os.listdir(query_dir):
            if filename.endswith(".json"):
                file_path = os.path.join(query_dir, filename)
                with open(file_path, "r", encoding="utf-8") as f:
                    query_record = json.load(f)
                    queries.append(query_record)
        
        # 按时间戳降序排序
        queries.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {"queries": queries}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))