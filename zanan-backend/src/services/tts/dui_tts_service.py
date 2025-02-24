from typing import Optional
import os
import aiohttp
from urllib.parse import quote
import asyncio

class DuiTTSService:
    """讯飞开放平台文本转语音服务
    
    使用讯飞开放平台的 TTS 服务实现多语言的语音生成功能。
    支持四川话、粤语等多种方言的语音生成。
    """
    
    def __init__(self):
        # 语言代码映射到声音ID
        self.voice_map = {
            "zh-sc": "wqingf_csn",    # 四川话女声音色偏甜美自然
            "zh-yue": "lunaif_ctn",  # 粤语女声偏正式的标准粤语
            "zh": "qiumum_0gushi",   # 普通话活泼开朗
        }
        
        # API 基础URL
        self.base_url = "https://dds.dui.ai/runtime/v1/synthesize"
        
        # 重试配置
        self.max_retries = 3
        self.retry_delay = 1  # 重试间隔（秒）
    
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
        # 获取对应语言的声音ID
        voice_id = self.voice_map.get(language.lower())
        if not voice_id:
            print(f"不支持的语言: {language}")
            return None
        
        # 构建API请求URL
        params = {
            "voiceId": voice_id,
            "text": quote(text),
            "speed": 1,
            "volume": 50,
            "audioType": "wav"
        }
        url = f"{self.base_url}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
        
        # 实现重试机制
        for attempt in range(self.max_retries):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=30) as response:  # 添加超时设置
                        if response.status == 200:
                            with open(output_path, 'wb') as f:
                                f.write(await response.read())
                            return os.path.basename(output_path)
                        else:
                            print(f"API请求失败 (尝试 {attempt + 1}/{self.max_retries}): HTTP {response.status}")
                            
            except aiohttp.ClientError as e:
                print(f"网络连接错误 (尝试 {attempt + 1}/{self.max_retries}): {str(e)}")
            except asyncio.TimeoutError:
                print(f"请求超时 (尝试 {attempt + 1}/{self.max_retries})")
            except Exception as e:
                error_msg = str(e).encode('unicode_escape').decode('utf-8')
                print(f"语音生成错误 (尝试 {attempt + 1}/{self.max_retries}): {error_msg}")
            
            # 如果不是最后一次尝试，则等待后重试
            if attempt < self.max_retries - 1:
                await asyncio.sleep(self.retry_delay)
            
        print("已达到最大重试次数，生成音频失败")
        return None