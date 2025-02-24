#!/bin/bash

# 进入后端目录
cd zanan-backend || {
    echo "错误：无法进入后端目录"
    exit 1
}

# 检查虚拟环境是否存在
if [ ! -d "venv" ]; then
    echo "创建新的虚拟环境..."
    python3 -m venv venv || {
        echo "错误：无法创建虚拟环境"
        exit 1
    }
fi

# 激活虚拟环境
echo "激活虚拟环境..."
source venv/bin/activate || {
    echo "错误：无法激活虚拟环境"
    exit 1
}

# 确认虚拟环境已激活
if [ -z "$VIRTUAL_ENV" ]; then
    echo "错误：虚拟环境未正确激活"
    exit 1
fi

# 更新 pip
echo "更新 pip..."
pip install --upgrade pip

# 安装依赖
echo "安装项目依赖..."
pip install -r requirements.txt || {
    echo "错误：安装依赖失败"
    deactivate
    exit 1
}

echo "\n依赖安装完成！"
echo "提示：使用 'deactivate' 命令可以退出虚拟环境"