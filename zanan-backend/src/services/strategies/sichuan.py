from typing import List
from .language_strategy import LanguageStrategy
from ..audio_base import AudioGeneratorStrategy

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
            prompt = f"请提供词语 '{word}' 的四川话解释和注音。要求：\n1. 使用简体字\n2. 解释要简洁易懂，使用地道的四川话表达\n3. 使用四川话拼音注音（参考汉语拼音，标注声调）\n4. 按以下格式回复：\n解释：[四川话解释]\n音标：[四川话拼音]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # 解析响应文本
                lines = response.strip().split('\n')
                definition = ""
                phonetic = ""
                
                for line in lines:
                    if line.startswith("解释："):
                        definition = line.replace("解释：", "").strip()
                    elif line.startswith("音标："):
                        phonetic = line.replace("音标：", "").strip()
                
                return {"definition": definition, "phonetic": phonetic}
                
        except Exception as e:
            print(f"[SichuaneseStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": ""}
    
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
                prompt = f"请将以下英语句子翻译成四川话（使用简体字），不需要解释：\n{example}"
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