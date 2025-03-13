from typing import List
from .language_strategy import LanguageStrategy
from ..audio_base import AudioGeneratorStrategy
from ..utils.language_utils import LanguageUtils

class MandarinStrategy(LanguageStrategy):
    """普通话策略实现类"""
    def __init__(self):
        """初始化普通话策略"""
        super().__init__()
        from ..llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "zh"
        
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
        
        使用 LLM 服务生成普通话定义和音标。
        
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
                prompt = f"请将英文单词 '{word}' 翻译成中文。要求：\n1. 只返回对应的中文词，不要其他解释\n2. 如果有多个含义，只返回最常用的一个"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                if response and isinstance(response, str):
                    pronounce_word = response.strip()
            
            prompt = f"请提供词语 '{pronounce_word}' 的中文（普通话）解释和拼音。要求：\n1. 使用简体字\n2. 解释要简洁易懂\n3. 使用汉语拼音注音（包含声调）\n4. 按以下格式回复：\n解释：[中文解释]\n拼音：[汉语拼音]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # 解析响应文本
                lines = response.strip().split('\n')
                definition = ""
                phonetic = ""
                
                for line in lines:
                    if line.startswith("解释："):
                        definition = line.replace("解释：", "").strip()
                    elif line.startswith("拼音："):
                        phonetic = line.replace("拼音：", "").strip()
                
                return {"definition": definition, "phonetic": phonetic, "pronounce_word": pronounce_word}
                
        except Exception as e:
            print(f"[MandarinStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": "", "pronounce_word": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到普通话
        
        使用 LLM 服务将英语例句翻译成普通话。
        
        参数:
            examples (List[str]): 要翻译的英语例句列表
            
        返回:
            List[str]: 翻译后的普通话例句列表
        """
        translated = []
        for example in examples:
            try:
                # 使用 LLM 服务翻译
                prompt = f"请将以下英语句子翻译成地道的普通话（使用简体字）。要求：\n1. 使用日常对话中常见的表达方式\n2. 确保符合普通话的语法结构和表达习惯\n3. 翻译要自然流畅，避免生硬的直译\n4. 只返回翻译后的句子，不要添加任何其他说明\n5. 翻译的句子中不要出现字母和符号，只包含中文\n句子：{example}"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                if response and isinstance(response, str):
                    translated.append(response)
                else:
                    print(f"[MandarinStrategy] LLM 服务返回无效结果，例句: {example}")
                    translated.append(example)
                    
            except Exception as e:
                print(f"[MandarinStrategy] 翻译错误: {e}, 例句: {example}")
                translated.append(example)
                
        return translated