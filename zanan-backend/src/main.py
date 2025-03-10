from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.word_controller import router as word_router
from .api.audio_controller import router as audio_router

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(word_router)
app.include_router(audio_router)