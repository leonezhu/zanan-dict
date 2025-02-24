from typing import Dict, Optional
from ...utils.audio_base import AudioGeneratorStrategy
from .edge_tts_generator import EdgeTTSGenerator
from .dui_tts_generator import DuiTTSGenerator

class TTSStrategyManager:
    """TTS 策略管理器
    
    根据不同语言选择合适的 TTS 实现。
    支持多种 TTS 服务的灵活切换。
    """
    
    def __init__(self, storage_dir: str):
        """初始化 TTS 策略管理器
        
        参数:
            storage_dir (str): 音频文件存储目录
        """
        # 初始化 TTS 生成器
        self.edge_tts = EdgeTTSGenerator(storage_dir)
        self.dui_tts = DuiTTSGenerator(storage_dir)
        
        # 配置语言到 TTS 生成器的映射
        self.language_tts_map = {
            "en": self.edge_tts,      # 英语使用 Edge TTS
            "zh": self.edge_tts,     # 普通话使用 Edge TTS
            "zh-yue": self.edge_tts, # 粤语使用 Edge TTS
            "zh-sc": self.dui_tts    # 四川话使用讯飞 TTS
        }
    
    def get_tts_generator(self, language: str) -> AudioGeneratorStrategy:
        """获取指定语言的 TTS 生成器
        
        参数:
            language (str): 目标语言代码
            
        返回:
            AudioGeneratorStrategy: 对应语言的 TTS 生成器
        """
        return self.language_tts_map.get(language.lower(), self.edge_tts)
    
    async def generate_audio(self, text: str, language: str, word: str) -> Optional[str]:
        """生成音频文件
        
        根据语言选择合适的 TTS 生成器来生成音频。
        
        参数:
            text (str): 要转换的文本内容
            language (str): 目标语言代码
            word (str): 相关单词，用于生成文件名
            
        返回:
            Optional[str]: 成功时返回音频文件的URL路径，失败时返回 None
        """
        generator = self.get_tts_generator(language)
        return await generator.generate_audio(text, language, word)