try:
    from .config_local import LLM_CONFIG_LOCAL
except ImportError:
    LLM_CONFIG_LOCAL = {}

# 全局存储路径配置
STORAGE_DIR = "storage"

LLM_CONFIG = {
    "siliconflow": {
        "api_url": "https://api.siliconflow.cn/v1/chat/completions",
        "api_key": LLM_CONFIG_LOCAL.get("siliconflow", {}).get("api_key", ""),
        "model": "Qwen/Qwen2-7B-Instruct"
    }
}
# add config_local.py than copy this 
LLM_CONFIG_LOCAL = {
    "siliconflow": {
        "api_key": "sk-xxx"
    }
}

# 提示词模板配置
PROMPT_TEMPLATES = {
    "definition": """请为词语 "{word}" 生成一个完整的定义。
要求：
1. 返回 JSON 格式的字符串
2. 包含以下字段：
   - definition: 单词的英文释义
   - phonetic: 音标
示例输出：
{{
    "definition": "A word used to express greeting or acknowledgment",
    "phonetic": "/həˈloʊ/"
}}
""",
    
    "examples": """请为词语 "{word}" 生成 {count} 个地道的英文例句。
要求：
1. 返回 JSON 格式的字符串
2. 包含一个例句数组
3. 每个例句应该自然、地道，体现单词的用法
示例输出：
{{
    "examples": [
        "Hello, how are you doing today?",
        "She said hello to everyone at the party."
    ]
}}
"""
}