from typing import List
from .language_strategy import LanguageStrategy
from ..audio_base import AudioGeneratorStrategy

class EnglishStrategy(LanguageStrategy):
    """英语策略实现类"""
    def __init__(self):
        """初始化英语策略"""
        super().__init__()
        from ..llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "en"
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """获取音频生成器
        
        返回:
            AudioGeneratorStrategy: 音频生成器实例
        """
        from ..tts.edge_tts_generator import EdgeTTSGenerator
        return EdgeTTSGenerator()

    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标
        
        使用 LLM 服务生成英语定义和音标。
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义和音标的字典
        """
        try:
            prompt = f"Please provide the definition and phonetic transcription of '{word}' in English. Format your response as follows:\nDefinition: [clear, concise definition]\nPhonetic: [IPA transcription]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # 解析响应文本
                lines = response.strip().split('\n')
                definition = ""
                phonetic = ""
                
                for line in lines:
                    if line.startswith("Definition:"):
                        definition = line.replace("Definition:", "").strip()
                    elif line.startswith("Phonetic:"):
                        phonetic = line.replace("Phonetic:", "").strip()
                
                return {"definition": definition, "phonetic": phonetic}
                
        except Exception as e:
            print(f"[EnglishStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子"""
        """英语不用实现这个方法，因为生成的模板例句就是英语的 """
        return examples