# Zanan Dictionary 后端服务

## 项目结构

```
zanan-backend/
├── README.md           # 项目说明文档
├── requirements.txt    # 项目依赖
├── .env.example       # 环境变量示例文件
└── src/               # 源代码目录
    ├── __init__.py
    ├── main.py        # 应用入口
    ├── api/           # API 路由模块
    │   ├── __init__.py
    │   └── routes.py
    ├── models/        # 数据模型
    │   ├── __init__.py
    │   └── schemas.py
    ├── services/      # 业务逻辑
    │   ├── __init__.py
    │   ├── dictionary.py
    │   └── storage.py
    └── utils/         # 工具函数
        ├── __init__.py
        └── audio.py
```

## 环境要求

- Python 3.8+

## 主要依赖

- FastAPI: 现代、快速的 Web 框架
- Uvicorn: ASGI 服务器
- Pydantic: 数据验证库

## 本地开发环境配置

1. 进入项目目录并创建虚拟环境：

```bash
# 进入项目根目录
cd zanan-backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 确认虚拟环境已激活（命令行前缀显示 (venv)）
python3 --version

# 退出虚拟环境
deactivate
```

注意事项：
- 如果激活命令失败，请确保 Python 和 venv 模块已正确安装
- Windows 用户如遇到执行策略限制，可以使用管理员权限运行 PowerShell 并执行：`Set-ExecutionPolicy RemoteSigned`
- 每次开发前都需要先激活虚拟环境
- 完成开发后建议退出虚拟环境

2. 安装项目依赖：

```bash
# 确保在虚拟环境中
pip3 install -r requirements.txt
```

3. 启动开发服务器：

```bash
# 在项目根目录下运行
uvicorn src.main:app --reload --port 8000
```

服务器将在 http://localhost:8000 启动，支持热重载。
可以通过 http://localhost:8000/docs 访问 API 文档。

## 开发注意事项

1. 始终在虚拟环境中进行开发。可以通过命令行前缀的 (venv) 来确认是否已激活虚拟环境。

2. 添加新的依赖时，请更新 requirements.txt：
```bash
pip freeze > requirements.txt
```

3. 如需修改服务器端口（默认 8000），可在启动命令中指定：
```bash
uvicorn src.main:app --reload --port <端口号>
```