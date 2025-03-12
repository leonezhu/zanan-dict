## 本地开发环境配置
0. 在zanan--backend目录下创建config_local.py文件，内容如下：
```
# 白嫖的硅基流动免费大模型，所以要配置对应 api_key
LLM_CONFIG_LOCAL = {
    "siliconflow": {
        "api_key": "sk-xxxx"
    }
}
```

1. 后端第一次执行：进入项目目录并创建虚拟环境：

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

**看到start-backend.sh 文件了吗，之后可以在根目录下一键运行后端**   
> ./start-backend.sh


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

3. 启动后端开发服务器：

```bash
# 在项目根目录下运行
uvicorn src.main:app --reload --port 8000
```

服务器将在 http://localhost:8000 启动，支持热重载。
可以通过 http://localhost:8000/docs 访问 API 文档。

4. 启动前端页面
```bash
# 进入项目根目录
cd zanan-frontend

# 执行命令
npm install #第一次需要安装依赖
npm run dev
```

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

## TODO
- [x] 对查询词本身进行翻译和转语音
- [✔] 前端添加随机按钮，随机查询一个词，可以设置哪些方面，比如职场、生活等
- [x] 页面右侧添加配置项，比如哪个语言用哪个发音等，所有的配置需要统一到一个 json 中
- [x] 优化定义的生成，中文类的定义应该是一样的，直接从英文翻译成中文即可
