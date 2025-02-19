import os
from gtts import gTTS
from typing import Optional

class AudioGenerator:
    """音频生成器类
    
    用于生成文本到语音的转换，并保存为音频文件。
    支持多语言文本转语音，使用 Google Text-to-Speech 服务。
    """
    
    def __init__(self, storage_dir: str):
        """初始化音频生成器
        
        参数:
            storage_dir (str): 音频文件存储目录
        """
        self.audio_dir = os.path.join(storage_dir, "audio")
        os.makedirs(self.audio_dir, exist_ok=True)
    
    def generate_audio(self, text: str, language: str, word: str) -> Optional[str]:
        """生成音频文件
        
        将给定文本转换为语音，并保存为 MP3 文件。
        
        参数:
            text (str): 要转换的文本内容
            language (str): 目标语言代码（如 'en', 'zh'）
            word (str): 相关单词，用于生成文件名
            
        返回:
            Optional[str]: 成功时返回音频文件的URL路径，失败时返回 None
        """
        try:
            # 创建 TTS 对象，使用目标语言的前两个字符作为语言代码
            tts = gTTS(text=text, lang=language.lower()[:2])
            
            # 生成唯一的文件名
            audio_filename = f"{word}_{language}_{hash(text)}.mp3"
            audio_path = os.path.join(self.audio_dir, audio_filename)
            
            # 保存音频文件
            tts.save(audio_path)
            
            # 返回相对URL路径
            return f"/audio/{audio_filename}"
            
        except Exception as e:
            print(f"音频生成错误: {e}")
            return None