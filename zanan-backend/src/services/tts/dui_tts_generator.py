from typing import Optional
import asyncio
from src.utils.audio_base import BaseAudioGenerator
from src.services.tts.dui_tts_service import DuiTTSService

class DuiTTSGenerator(BaseAudioGenerator):
    """讯飞开放平台音频生成器实现类
    
    使用讯飞开放平台的 TTS 服务生成音频文件。
    专门用于四川话的语音生成。
    
    支持的语言代码：
    - zh-sc: 四川话
    """
    
    def __init__(self):
        """初始化讯飞开放平台音频生成器
        """
        super().__init__()
        self.tts_service = DuiTTSService()
    
    async def generate_audio(self, text: str, language: str, word: str) -> Optional[str]:
        """生成音频文件
        
        将给定文本转换为语音，并保存为音频文件。
        仅支持四川话。
        
        参数:
            text (str): 要转换的文本内容
            language (str): 目标语言代码（'zh-sc'）
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
            return None