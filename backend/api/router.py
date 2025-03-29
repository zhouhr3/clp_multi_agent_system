"""
API路由配置
"""
from fastapi import APIRouter
from .endpoints import users, patients, analyses, treatment_guidelines, literatures

# 创建主路由
api_router = APIRouter()

# 注册各个端点路由
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(analyses.router, prefix="/analyses", tags=["analyses"])
api_router.include_router(treatment_guidelines.router, prefix="/guidelines", tags=["guidelines"])
api_router.include_router(literatures.router, prefix="/literature", tags=["literature"])
