from typing import List, Optional, Protocol
from ..audio_base import AudioGeneratorStrategy

class LanguageStrategy(Protocol):
    """语言策略接口
    
    定义了不同语言实现类需要实现的方法。
    """
    def __init__(self):
        """初始化语言策略
        """
        self.language_code = "zh"  # 默认语言代码
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """获取音频生成器
        
        返回:
            AudioGeneratorStrategy: 音频生成器实例
        """
        raise NotImplementedError
    
    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标"""
        ...
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到目标语言"""
        ...
        
    async def generate_audio(self, text: str, word: str) -> Optional[str]:
        """生成音频文件
        
        将给定文本转换为语音，并保存为音频文件。
        
        参数:
            text (str): 要转换的文本内容
            word (str): 相关单词，用于生成文件名
            
        返回:
            Optional[str]: 成功时返回音频文件的URL路径，失败时返回 None
        """
        return await self.tts_generator.generate_audio(text, self.language_code, word)