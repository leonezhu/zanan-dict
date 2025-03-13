from typing import List
from .language_strategy import LanguageStrategy
from ..audio_base import AudioGeneratorStrategy
from ..utils.language_utils import LanguageUtils

class SichuaneseStrategy(LanguageStrategy):
    """四川话策略实现类"""
    def __init__(self):
        """初始化四川话策略"""
        super().__init__()
        from ..llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "zh-sc"
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """获取音频生成器
        
        返回:
            AudioGeneratorStrategy: 音频生成器实例
        """
        from ..tts.dui_tts_generator import DuiTTSGenerator
        return DuiTTSGenerator()

    async def generate_definition(self, word: str) -> dict:
        """生成单词定义和音标
        
        使用 LLM 服务生成四川话定义和音标。
        
        参数:
            word (str): 要查询的单词
            
        返回:
            dict: 包含定义和音标的字典
        """
        try:
            # 判断输入词是否为中文
            is_chinese_word = LanguageUtils.is_chinese(word)
            pronounce_word = word if is_chinese_word else ""
            
            # 如果不是中文词，需要翻译
            if not is_chinese_word:
                prompt = f"Please translate the English word '{word}' to Chinese. Requirements:\n1. Return ONLY the Chinese word\n2. If multiple meanings exist, return ONLY the most common one\n3. Do not include any explanations or additional text"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                if response and isinstance(response, str):
                    pronounce_word = response.strip()
            # 如果是中文词，转换为地道的四川话用词
            else:
                prompt = f"Translate '{word}' to Sichuan dialect. Requirements:\n1. Return ONLY the Sichuan dialect word in Simplified Chinese characters\n2. If multiple expressions exist, return ONLY the most commonly used one\n3. Do not include any explanations or additional text"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                if response and isinstance(response, str):
                    pronounce_word = response.strip()
            
            # 生成定义和音标
            prompt = f"Please provide the definition and phonetic transcription of '{pronounce_word}' in Sichuan dialect. Format your response as follows:\nDefinition: [clear and concise definition in Simplified Chinese]\nPhonetic: [Sichuan dialect phonetic transcription]"
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
                
                return {"definition": definition, "phonetic": phonetic, "pronounce_word": pronounce_word}
                
        except Exception as e:
            print(f"[SichuanStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": "", "pronounce_word": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到四川话
        
        使用 LLM 服务将英语例句翻译成四川话。
        
        参数:
            examples (List[str]): 要翻译的英语例句列表
            
        返回:
            List[str]: 翻译后的四川话例句列表
        """
        translated = []
        for example in examples:
            try:
                # 使用 LLM 服务翻译
                prompt = f"Please translate the following English sentence to Sichuan dialect (using Simplified Chinese characters). Requirements:\n1. Use natural, everyday Sichuan dialect expressions\n2. Ensure the translation follows Sichuan dialect grammar and speaking habits\n3. The translation should be fluent and natural, avoid literal translations\n4. Return ONLY the translated sentence, no additional explanations\n5. Use only Chinese characters, no letters or symbols\nSentence: {example}"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                if response and isinstance(response, str):
                    translated.append(response)
                else:
                    print(f"[SichuaneseStrategy] LLM 服务返回无效结果，例句: {example}")
                    translated.append(example)
                    
            except Exception as e:
                print(f"[SichuaneseStrategy] 翻译错误: {e}, 例句: {example}")
                translated.append(example)
                
        return translated