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
4. 例句中只出现英文，如果有中文名词或地面翻译成拼音
示例输出：
{{
    "examples": [
        "Hello, how are you doing today?",
        "She said hello to everyone at the party."
    ]
}}
""",

    "random_word": """请根据以下条件生成一个英文单词：
1. 风格类型：{style}
2. 时间戳：{timestamp}
3. 风格详细说明：
   - work: 与工作、职场相关的词汇
   - life: 日常生活中常用的词汇
   - computer: 计算机、技术相关的词汇
   - study: 学术、教育相关的词汇

要求：
1. 返回 JSON 格式的字符串
2. 包含一个 word 字段
3. 单词应该是常用的、适合学习的英文单词
4. 根据时间戳作为随机种子，生成不同的单词
5. 确保生成的单词与指定的风格类型相符

示例输出：
{{
    "word": "collaboration"
}}
"""

}