from typing import Dict, List, Optional, Protocol
import os

class AudioGeneratorStrategy(Protocol):
    """音频生成器策略接口
    
    定义了不同语言音频生成实现类需要实现的方法。
    """
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
        raise NotImplementedError

class BaseAudioGenerator:
    """音频生成器基类
    
    提供基础的文件存储和路径管理功能。
    """
    def __init__(self, storage_dir: str):
        """初始化音频生成器
        
        参数:
            storage_dir (str): 音频文件存储目录
        """
        self.audio_dir = os.path.join(storage_dir, "audio")
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def get_audio_path(self, word: str, language: str, text: str) -> str:
        """生成音频文件路径
        
        参数:
            word (str): 相关单词
            language (str): 目标语言代码
            text (str): 文本内容
            
        返回:
            str: 音频文件路径
        """
        audio_filename = f"{word}_{language}_{hash(text)}.mp3"
        return os.path.join(self.audio_dir, audio_filename)