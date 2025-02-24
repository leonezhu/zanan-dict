from typing import Optional
import asyncio
import os
from ...utils.audio_base import BaseAudioGenerator
from .tts_service import TTSService

class EdgeTTSGenerator(BaseAudioGenerator):
    """Edge TTS 音频生成器实现类
    
    使用 Edge TTS 服务生成音频文件。
    支持多种语言的语音生成。
    """
    
    def __init__(self, storage_dir: str):
        """初始化 Edge TTS 音频生成器
        
        参数:
            storage_dir (str): 音频文件存储目录
        """
        super().__init__(storage_dir)
        self.tts_service = TTSService()
    
    async def generate_audio(self, text: str, language: str, word: str) -> Optional[str]:
        """生成音频文件
        
        将给定文本转换为语音，并保存为 MP3 文件。
        
        参数:
            text (str): 要转换的文本内容
            language (str): 目标语言代码（如 'en', 'zh'）
            word (str): 相关单词，用于生成文件名
            
        返回:
            Optional[str]: 成功时返回音频文件的URL路径，失败时返回 None
        """
        if not text or not language or not word:
            return None
            
        try:
            # 获取音频文件路径
            audio_path = self.get_audio_path(word, language, text)
            
            # 使用 TTS 服务生成音频
            result = await self.tts_service.generate_speech(text, language, audio_path)
            if not result:
                print("TTS 服务生成音频失败")
                return None
                
            # 返回标准化的音频URL路径
            return result
            
        except asyncio.CancelledError:
            print("音频生成任务被取消")
            return None
        except Exception as e:
            print(f"音频生成错误: {str(e)}")
            # 确保错误信息不包含可能导致 JSON 解析错误的特殊字符
            return None