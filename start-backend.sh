#!/bin/bash

# 进入后端目录
cd zanan-backend

# 激活虚拟环境
source venv/bin/activate

# 启动服务器
uvicorn src.main:app --reload --port 8000

# 如果服务器停止，自动退出虚拟环境
deactivate