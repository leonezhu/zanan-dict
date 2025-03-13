from typing import List
from .language_strategy import LanguageStrategy
from ..audio_base import AudioGeneratorStrategy
from ..utils.language_utils import LanguageUtils

class CantoneseStrategy(LanguageStrategy):
    """粤语策略实现类"""
    def __init__(self):
        """初始化粤语策略"""
        super().__init__()
        from ..llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "zh-yue"
        
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
        
        使用 LLM 服务生成粤语定义和音标。
        
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
            
            # 生成定义和音标
            prompt = f"请提供单词 '{pronounce_word}' 的广东话（粤语）解释及粤语拼音。要求：\n1. 只使用繁体字，不要英文。\n2. 解释简洁易懂，避免混杂其他语言或符号。\n3. 使用标准粤语拼音（粤拼）注音。\n4. 按以下格式回复：\n解释： [广东话解释]\n粤拼： [粤语拼音]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # 解析响应文本
                lines = response.strip().split('\n')
                definition = ""
                phonetic = ""
                
                for line in lines:
                    if line.startswith("解释："):
                        definition = line.replace("解释：", "").strip()
                    elif line.startswith("粤拼："):
                        phonetic = line.replace("粤拼：", "").strip()
                
                return {"definition": definition, "phonetic": phonetic, "pronounce_word": pronounce_word}
                
        except Exception as e:
            print(f"[CantoneseStrategy] 生成定义错误: {e}")
            
        return {"definition": "", "phonetic": "", "pronounce_word": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """翻译示例句子到粤语
        
        使用 LLM 服务将英语例句翻译成粤语。
        
        参数:
            examples (List[str]): 要翻译的英语例句列表
            
        返回:
            List[str]: 翻译后的粤语例句列表
        """
        translated = []
        for example in examples:
            try:
                # 使用 LLM 服务翻译
                prompt = f"请将以下英语句子翻译成地道的广东话（使用繁体字）。要求：\n0.只要繁体字，不要英文\n1. 使用日常口语中的粤语表达。\n2. 确保语法和表达符合粤语习惯。\n3. 翻译自然流畅，避免生硬的直译。\n4. 仅返回翻译后的句子，不要附加说明。\n句子：{example}"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                if response and isinstance(response, str):
                    translated.append(response)
                else:
                    print(f"[CantoneseStrategy] LLM 服务返回无效结果，例句: {example}")
                    translated.append(example)
                    
            except Exception as e:
                print(f"[CantoneseStrategy] 翻译错误: {e}, 例句: {example}")
                translated.append(example)
                
        return translated