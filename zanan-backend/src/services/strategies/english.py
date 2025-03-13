from typing import List
from .language_strategy import LanguageStrategy
from ..audio_base import AudioGeneratorStrategy
from ..utils.language_utils import LanguageUtils

class EnglishStrategy(LanguageStrategy):
    """English strategy implementation class"""
    def __init__(self):
        """Initialize English strategy"""
        super().__init__()
        from ..llms.llm_service import LLMService
        self.llm_service = LLMService()
        self.language_code = "en"
        
    @property
    def tts_generator(self) -> AudioGeneratorStrategy:
        """Get audio generator
        
        Returns:
            AudioGeneratorStrategy: Audio generator instance
        """
        from ..tts.edge_tts_generator import EdgeTTSGenerator
        return EdgeTTSGenerator()

    async def generate_definition(self, word: str) -> dict:
        """Generate word definition and phonetic transcription
        
        Use LLM service to generate English definition and phonetic transcription.
        
        Args:
            word (str): The word to query
            
        Returns:
            dict: Dictionary containing definition and phonetic transcription
        """
        try:
            # Check if input word is Chinese
            is_chinese_word = LanguageUtils.is_chinese(word)
            pronounce_word = word
            
            # If it's a Chinese word, translate to English
            if is_chinese_word:
                prompt = f"Translate '{word}' to English. Requirements:\n1. Return ONLY the English word\n2. If multiple meanings exist, return ONLY the most common one\n3. Do not include any explanations or additional text"
                response = await self.llm_service.get_examples_with_prompt(prompt)
                if response and isinstance(response, str):
                    pronounce_word = response.strip()
            
            prompt = f"Please provide the definition and phonetic transcription of '{pronounce_word}' in English. Format your response as follows:\nDefinition: [clear, concise definition]\nPhonetic: [IPA transcription]"
            response = await self.llm_service.get_examples_with_prompt(prompt)
            
            if response and isinstance(response, str):
                # Parse response text
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
            print(f"[EnglishStrategy] Definition generation error: {e}")
            
        return {"definition": "", "phonetic": "", "pronounce_word": ""}
    
    async def translate_examples(self, examples: List[str]) -> List[str]:
        """Translate example sentences"""
        """This method doesn't need implementation for English since template sentences are already in English"""
        return examples