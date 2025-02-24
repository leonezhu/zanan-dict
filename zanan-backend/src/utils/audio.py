from typing import Optional
import os
from .audio_base import BaseAudioGenerator, AudioGeneratorStrategy
from ..services.tts.tts_strategy import TTSStrategyManager


class MockAudioGenerator(BaseAudioGenerator):
    """模拟音频生成器实现类
    
    用于测试和开发环境，不实际生成音频文件。
    """
    async def generate_audio(self, text: str, language: str, word: str) -> Optional[str]:
        # 模拟生成音频文件路径
        audio_path = self.get_audio_path(word, language, text)
        return f"/audio/{os.path.basename(audio_path)}"

# 选择 TTS 生成器
AudioGenerator = TTSStrategyManager