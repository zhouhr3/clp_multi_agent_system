"""
用户模型的API模式定义
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 用户基础模式
class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100)
    
# 用户创建请求模式
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
# 用户更新请求模式
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    password: Optional[str] = Field(None, min_length=8)
    is_active: Optional[bool] = None
    
# 用户响应模式
class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
        
# 用户登录请求模式
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
# 令牌响应模式
class Token(BaseModel):
    access_token: str
    token_type: str
    
# 令牌数据模式
class TokenData(BaseModel):
    user_id: Optional[int] = None
