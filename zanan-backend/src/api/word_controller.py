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
    try:
        # 参数验证
        if not request.word:
            raise HTTPException(status_code=400, detail="单词不能为空")
        if not request.languages:
            raise HTTPException(status_code=400, detail="至少需要指定一种目标语言")
        
        print(f"request: {request}")
        # 调用服务层处理查询
        result = await dictionary_service.query_word(request.word, request.languages, request.example_count)
        
        # 直接返回服务层生成的结果
        return result
        
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

@router.delete("/api/queries/{timestamp}")
async def delete_query_record(timestamp: float):
    """删除指定的查询记录
    
    根据时间戳删除对应的查询记录文件。
    
    参数:
        timestamp (float): 查询记录的时间戳
    
    返回:
        dict: 删除操作的结果
    
    异常:
        HTTPException: 当删除失败时抛出异常
    """
    try:
        query_dir = dictionary_service.query_dir
        if not os.path.exists(query_dir):
            raise HTTPException(status_code=404, detail="查询记录目录不存在")
        
        # 查找对应时间戳的文件
        target_file = None
        for filename in os.listdir(query_dir):
            if filename.endswith(".json"):
                file_timestamp = float(filename.split("_")[1].replace(".json", ""))
                if abs(file_timestamp - timestamp) < 0.001:  # 使用小数点后三位进行比较
                    target_file = filename
                    break
        
        if not target_file:
            raise HTTPException(status_code=404, detail="未找到指定的查询记录")
        
        # 删除文件
        file_path = os.path.join(query_dir, target_file)
        os.remove(file_path)
        
        return {"message": "查询记录已删除"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))