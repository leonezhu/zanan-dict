from typing import Dict, List, Optional, Protocol
from .siliconflow import SiliconFlowLLM
from ...config import PROMPT_TEMPLATES

class LLMServiceProtocol(Protocol):
    """LLM 服务接口
    
    定义了与 LLM 服务交互所需的方法。
    """
    async def generate_word_definition(self, word: str) -> dict:
        """生成单词定义
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义、音标等信息的字典
        """
        ...
    
    async def generate_examples(self, word: str, count: int = 5) -> List[str]:
        """生成示例句子
        
        参数:
            word (str): 要使用的单词
            count (int): 需要生成的例句数量
            
        返回:
            List[str]: 生成的示例句子列表
        """
        ...

class DemoLLMService:
    """示例 LLM 服务实现
    
    用于开发和测试环境。实际项目中需要替换为真实的 LLM 服务实现。
    """
    async def generate_word_definition(self, word: str) -> dict:
        """生成单词定义（示例实现）
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义、音标等信息的字典
        """
        return {
            "definition": f"Definition for {word}",
            "phonetic": f"/{word}/",
            "pos": "n.",
            "synonyms": [f"syn1_{word}", f"syn2_{word}"],
            "antonyms": [f"ant1_{word}", f"ant2_{word}"]
        }
    
    async def generate_examples(self, word: str, count: int = 5) -> List[str]:
        """生成示例句子（示例实现）
        
        参数:
            word (str): 要使用的单词
            count (int): 需要生成的例句数量
            
        返回:
            List[str]: 生成的示例句子列表
        """
        examples = [
            f"How are you using {word} today?",
            f"Nice to learn the word {word}!",
            f"Welcome to our {word} meeting.",
            f"What's the {word} like?",
            f"Can you help me with {word}?"
        ]
        return examples[:count]

class LLMService:
    """实际的 LLM 服务实现
    
    使用 SiliconFlow LLM 实现单词定义和例句生成功能。
    """
    def __init__(self):
        self.llm = SiliconFlowLLM()

    async def generate_word_definition(self, word: str) -> dict:
        """生成单词定义
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义、音标等信息的字典
        """
        response = await self.llm.generate_definition(word, "english")
        if response:
            try:
                import json
                result = json.loads(response)
                return {
                    "definition": result.get("definition", f"Definition for {word}"),
                    "phonetic": result.get("phonetic", f"/{word}/"),
                    "pos": result.get("pos", "n."),
                    "synonyms": result.get("synonyms", []),
                    "antonyms": result.get("antonyms", [])
                }
            except json.JSONDecodeError:
                print(f"JSON 解析错误: {response}")
        
        # 如果 API 调用失败或解析错误，返回默认值
        return {
            "definition": f"Definition for {word}",
            "phonetic": f"/{word}/",
            "pos": "n.",
            "synonyms": [],
            "antonyms": []
        }

    async def generate_examples(self, word: str, count: int = 5) -> List[str]:
        """生成示例句子
        
        参数:
            word (str): 要使用的单词
            count (int): 需要生成的例句数量
            
        返回:
            List[str]: 生成的示例句子列表
        """
        response = await self.get_examples(word, "english", count)
        if response:
            try:
                import json
                print(f"LLM API 原始响应: {response}")
                result = json.loads(response)
                examples = result.get("examples", [])
                print(f"解析后的例句: {examples}")
                return examples
            except json.JSONDecodeError as e:
                print(f"JSON 解析错误: {str(e)}\n原始响应: {response}")
                return []
            except Exception as e:
                print(f"LLM 服务调用错误: {str(e)}\n原始响应: {response}")
                return []
        return []

    async def get_examples_with_prompt(self, prompt: str) -> Optional[str]:
        """使用自定义提示词生成内容

        Args:
            prompt (str): 自定义提示词

        Returns:
            Optional[str]: 生成的内容，如果请求失败则返回 None
        """
        return await self.llm.generate_response(prompt)

    async def get_examples(self, word: str, language: str, count: int = 3) -> Optional[str]:
        """使用预设模板生成例句

        Args:
            word (str): 需要生成例句的单词
            language (str): 目标语言
            count (int, optional): 需要生成的例句数量. 默认为 3.

        Returns:
            Optional[str]: 生成的例句，如果请求失败则返回 None
        """
        prompt = PROMPT_TEMPLATES["examples"].format(
            word=word,
            language=language,
            count=count
        )
        return await self.llm.generate_response(prompt)

    _recent_words = []  # 类变量，用于存储最近生成的单词
    _max_recent_words = 50  # 最多保存的最近单词数量

    async def generate_random_word(self, style: str) -> Optional[str]:
        """生成随机单词

        Args:
            style (str): 单词风格，可选值：work, life, computer, study

        Returns:
            Optional[str]: 生成的单词，如果请求失败则返回 None
        """
        import time
        current_timestamp = int(time.time())
        prompt = PROMPT_TEMPLATES["random_word"].format(
            style=style,
            timestamp=current_timestamp  # 将时间戳作为随机种子传入模板
        )
        
        max_attempts = 3  # 最大尝试次数
        for _ in range(max_attempts):
            response = await self.llm.generate_response(prompt)
            if response:
                try:
                    import json
                    result = json.loads(response)
                    word = result.get("word")
                    
                    # 如果生成的单词在最近列表中，继续尝试
                    if word in self._recent_words:
                        continue
                        
                    # 将新单词添加到最近列表
                    self._recent_words.append(word)
                    # 如果列表超过最大长度，移除最早的单词
                    if len(self._recent_words) > self._max_recent_words:
                        self._recent_words.pop(0)
                        
                    return word
                except json.JSONDecodeError:
                    print(f"JSON 解析错误: {response}")
                except Exception as e:
                    print(f"生成随机单词错误: {str(e)}")
        return None