from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .api.router import api_router
from .api.dependencies import get_db
from .config.settings import settings
from .models.base import Base
from .utils.database import engine

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="基于人工智能的唇腭裂多智能体医疗辅助决策系统",
    version="1.0.0",
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "欢迎使用唇腭裂多智能体系统API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
