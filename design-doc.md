# 多语言词汇查询与发音生成系统设计文档

## 1. 项目概述

本项目旨在开发一个支持多语言词汇查询与发音生成的系统。用户可以输入特定的单词或短语，选择目标语言，系统将返回该词汇在指定语言中的定义、音标、发音以及示例句子和其发音。初期支持英语和粤语，未来将扩展至普通话、四川话等其他方言。

## 2. 需求描述

### 2.1 功能需求

1. **多语言选择**：用户可以选择多种语言进行查询，如英语、粤语、普通话、四川话等。
2. **词汇查询**：输入一个英文单词或中文词语，系统返回各语言的解释、音标、发音和示例句子。
3. **示例句子生成**：为查询的词汇生成对应语言的示例句子，并提供发音。
4. **查询记录存储**：保存每次查询的记录，供用户日后查看。

### 2.2 非功能需求

1. **可扩展性**：系统架构应支持后续添加新语言和更换或增加大模型。
2. **性能**：对于多语言查询，后端应采用异步处理，提高响应速度。
3. **存储**：初期使用本地存储查询记录，未来可扩展至数据库存储。

## 3. 系统架构设计

### 3.1 总体架构

系统采用前后端分离架构：

- **前端**：提供用户交互界面，允许用户输入查询词汇，选择目标语言，并展示查询结果和历史记录。
- **后端**：处理前端请求，进行词汇查询、示例句子生成、发音生成，并将查询记录保存。

### 3.2 后端架构

后端由以下模块组成：

1. **API 层**：接收前端请求，进行参数验证和路由。
2. **处理层**：
   - **词典查询模块**：根据输入词汇和语言，查询对应的定义和音标。
   - **示例句子生成模块**：调用大模型生成对应语言的示例句子。
   - **文本转语音（TTS）模块**：将文本内容转换为语音。
3. **存储层**：保存查询记录，初期采用本地 JSON 文件存储，未来可扩展为数据库存储。

### 3.3 模块化设计

各模块设计为独立组件，方便后续扩展和维护。例如，新增语言时，只需添加相应的词典查询和TTS模块。

## 4. 接口设计

### 4.1 查询接口

**请求方式**：`POST /api/query`

**请求示例**：

```json
{
  "word": "hello",
  "languages": ["en", "zh-yue"]
}
```

**响应示例**：

```json
{
  "word": "hello",
  "results": {
    "en": {
      "definition": "A greeting or expression of goodwill.",
      "phonetic": "/həˈloʊ/",
      "pronunciation": "/本地目录/audio/hello_en.mp3",
      "example_sentence": "Hello, how are you?",
      "sentence_pronunciation": "/本地目录/audio/hello_sentence_en.mp3"
    },
    "zh-yue": {
      "definition": "用于问候他人的词语",
      "phonetic": "hē-lóu",
      "pronunciation": "http://example.com/audio/hello_zh-yue.mp3",
      "example_sentence": "你好，最近怎么样？",
      "sentence_pronunciation": "http://example.com/audio/hello_sentence_zh-yue.mp3"
    }
  }
}
```

### 4.2 查询记录接口

**请求方式**：`GET /api/queries`

**响应示例**：

```json
{
  "queries": [
    {
      "word": "hello",
      "languages": ["en", "zh-yue"],
      "results": { ... },
      "timestamp": "2025-02-19T14:07:50Z"
    },
    ...
  ]
}
```

## 5. 异步处理与性能优化

为提高多语言查询的响应速度，后端采用异步处理方式。对于每个语言的查询，启动独立的异步任务并行处理，待所有任务完成后统一返回结果。

示例代码（使用 Python 的 `asyncio`）：

```python
import asyncio

async def process_language(word, language):
    # 模拟异步处理，如调用外部API或大模型
    await asyncio.sleep(1)  # 模拟延迟
    return { "definition": f"{word} in {language}", "phonetic": "..." }

async def query_word(word, languages):
    tasks = [process_language(word, lang) for lang in languages]
    results = await asyncio.gather(*tasks)
    return { lang: result for lang, result in zip(languages, results) }
```

## 6. 查询记录存储

初期采用本地 JSON 文件存储查询记录。每次查询后，将记录保存至指定目录，文件名可使用时间戳或UUID。

示例代码：

```python
import json
import os
from datetime import datetime

QUERY_DIR = "queries/"

def save_query_record(word, languages, results):
    os.makedirs(QUERY_DIR, exist_ok=True)
    record = {
        "word": word,
        "languages": languages,
        "results": results,
        "timestamp": datetime.utcnow().isoformat()
    }
    filename = os.path.join(QUERY_DIR, f"{word}_{datetime.utcnow().timestamp()}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=4)
```

## 7. 扩展性考虑

- **新增语言支持**：添加新的语言或方言时，需扩展词典查询模块和TTS模块，并在接口中支持新的语言标识。
- **大模型替换**：处理层设计为可插拔式，方便更换或增加新的大模型。
- **存储升级**：当查询记录增多时，可将存储层升级为数据库（如SQLite、MySQL）以提高性能和管理效率。

## 8. 技术栈

- **后端框架**：FastAPI（支持异步处理，性能优越）
- **大模型接口**：OpenAI GPT 系列或 Hugging Face 模型
- **文本转语音**：Google TTS、Mozilla TTS，或其他支持目标语言的TTS服务
- **存储**：初期使用本地文件，未来可扩展为数据库

