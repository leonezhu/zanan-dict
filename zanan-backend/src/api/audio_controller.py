from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/api/audio/{filename}")
async def get_audio(filename: str):
    """
    获取音频文件
    
    参数:
        filename (str): 音频文件名
    
    返回:
        FileResponse: 音频文件的响应
    
    异常:
        HTTPException: 当文件不存在时抛出异常
    """
    try:
        print("filename", filename)
        # 获取音频文件的完整路径
        audio_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "storage", "audio", filename)
        
        # 检查文件是否存在
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="音频文件不存在")
        
        # 返回音频文件
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename=filename
        )
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))



        