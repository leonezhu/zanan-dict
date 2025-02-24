import aiohttp
from typing import Dict, Any, Optional
from ...config import LLM_CONFIG

class SiliconFlowLLM:
    def __init__(self):
        config = LLM_CONFIG["siliconflow"]
        self.api_url = config["api_url"]
        self.api_key = config["api_key"]
        self.model = config["model"]
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def generate_response(self, prompt: str) -> Optional[str]:
        """发送请求到硅基流动API并获取响应

        Args:
            prompt (str): 提示词

        Returns:
            Optional[str]: 生成的响应文本，如果请求失败则返回 None
        """
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "你是一个词典助手。"},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, headers=self.headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        print(f"API 响应数据: {result}")
                        content = result['choices'][0]['message']['content']
                        print(f"提取的内容: {content}")
                        return content
                    else:
                        print(f"请求失败，状态码：{response.status}，响应内容：{await response.text()}")
                        return None
        except Exception as e:
            print(f"请求发生错误：{str(e)}，请求数据：{data}")
            return None

    async def generate_examples(self, word: str, language: str, count: int = 3) -> Optional[str]:
        """生成指定单词的例句

        Args:
            word (str): 需要生成例句的单词
            language (str): 目标语言
            count (int, optional): 需要生成的例句数量. 默认为 3.

        Returns:
            Optional[str]: 生成的例句，如果请求失败则返回 None
        """
        prompt = f"请用 {language} 为单词 '{word}' 生成 {count} 个地道的例句。"
        return await self.generate_response(prompt)

    async def generate_definition(self, word: str, language: str) -> Optional[str]:
        """生成指定单词的释义

        Args:
            word (str): 需要解释的单词
            language (str): 目标语言

        Returns:
            Optional[str]: 生成的释义，如果请求失败则返回 None
        """
        prompt = f"请提供单词 '{word}' 在 {language} 中的释义。"
        return await self.generate_response(prompt)
