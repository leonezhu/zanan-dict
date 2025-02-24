from typing import Dict, List, Optional
import os
import edge_tts
import asyncio

class TTSService:
    """文本转语音服务
    
    使用 Edge TTS 实现多语言的语音生成功能。
    支持英语和粤语等多种语言的语音生成。
    """
    
    def __init__(self):
        # 语言代码映射
        self.voice_map = {
            "en": "en-US-ChristopherNeural",  # 英语（美国）
            "zh-yue": "zh-HK-HiuGaaiNeural",  # 粤语（香港）
            "zh": "zh-CN-XiaoxiaoNeural",    # 普通话（中国大陆）
            "zh-sc": "zh-CN-YunxiNeural"     # 四川话暂时使用普通话声音
        }
    
    async def generate_speech(self, text: str, language: str, output_path: str) -> Optional[str]:
        """生成语音文件
        
        将文本转换为语音并保存为音频文件。
        
        参数:
            text (str): 要转换的文本
            language (str): 目标语言代码
            output_path (str): 输出文件路径
            
        返回:
            Optional[str]: 成功时返回音频文件的URL路径，失败时返回 None
        """
        try:
            # 获取对应语言的声音
            voice = self.voice_map.get(language.lower(), self.voice_map["en"])
            
            # 创建通信对象
            communicate = edge_tts.Communicate(text, voice)
            
            # 生成语音文件
            await communicate.save(output_path)
            
            # 返回文件名
            return os.path.basename(output_path)
            
        except Exception as e:
            error_msg = str(e).encode('unicode_escape').decode('utf-8')
            print(f"语音生成错误: {error_msg}")
            return None