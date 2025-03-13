try:
    from .config_local import LLM_CONFIG_LOCAL
except ImportError:
    LLM_CONFIG_LOCAL = {}

# Global storage path configuration
STORAGE_DIR = "storage"


# Qwen/Qwen2-7B-Instruct # *** 生成例句会有其他字符
# Qwen/Qwen2.5-7B-Instruct **
# deepseek-ai/DeepSeek-R1-Distill-Qwen-7B #不能用推理模型
# internlm/internlm2_5-7b-chat # 完美 速度有点慢
# THUDM/chatglm3-6b
LLM_CONFIG = {
    "siliconflow": {
        "api_url": "https://api.siliconflow.cn/v1/chat/completions",
        "api_key": LLM_CONFIG_LOCAL.get("siliconflow", {}).get("api_key", ""),
        "model": "internlm/internlm2_5-7b-chat"
    }
}
# add config_local.py than copy this 
LLM_CONFIG_LOCAL = {
    "siliconflow": {
        "api_key": "sk-xxx"
    }
}

# Prompt template configuration
PROMPT_TEMPLATES = {
    "definition": """Please generate a complete definition for the word "{word}".
Requirements:
1. Return a JSON string
2. Include the following fields:
   - definition: English definition of the word
   - phonetic: phonetic transcription
Example output:
{{
    "definition": "A word used to express greeting or acknowledgment",
    "phonetic": "/həˈloʊ/"
}}
""",
    
    "examples": """Please generate {count} authentic English sentences using the word "{word}".
Requirements:
1. Return a JSON string
2. Include an array of example sentences
3. Each sentence should be natural and idiomatic, demonstrating proper word usage
4. Sentences should only contain English; translate any proper nouns or place names to English or use pinyin
Example output:
{{
    "examples": [
        "Hello, how are you doing today?",
        "She said hello to everyone at the party."
    ]
}}
""",

    "random_word": """Please generate an English word based on the following conditions:
1. Style type: {style}
2. Timestamp: {timestamp}
3. Style specifications:
   - work: vocabulary related to work and professional settings
   - life: commonly used words in daily life
   - computer: vocabulary related to computers and technology
   - study: vocabulary related to academics and education

Requirements:
1. Return a JSON string
2. Include a word field
3. The word should be common and suitable for learning
4. Use the timestamp as a random seed to generate different words
5. Ensure the generated word matches the specified style type

Example output:
{{
    "word": "collaboration"
}}
"""

}