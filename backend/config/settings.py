import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # 应用设置
    APP_NAME: str = "唇腭裂多智能体系统"
    API_V1_STR: str = "/api/v1"
    
    # 安全设置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-development-only")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24小时
    
    # 数据库设置
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./cleft_multi_agent.db")
    
    # CORS设置
    CORS_ORIGINS: list = ["*"]
    
    # 外部API设置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    PUBMED_API_KEY: str = os.getenv("PUBMED_API_KEY", "")
    
    class Config:
        env_file = ".env"

settings = Settings()
