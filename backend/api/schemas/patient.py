"""
患者模型的API模式定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# 患者基础模式
class PatientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    age: str = Field(..., min_length=1, max_length=50)
    gender: str = Field(..., min_length=1, max_length=20)
    symptoms: List[str] = Field(..., min_items=1)
    medical_history: Optional[str] = None
    family_history: Optional[str] = None

# 患者创建请求模式
class PatientCreate(PatientBase):
    pass

# 患者更新请求模式
class PatientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    age: Optional[str] = Field(None, min_length=1, max_length=50)
    gender: Optional[str] = Field(None, min_length=1, max_length=20)
    symptoms: Optional[List[str]] = Field(None, min_items=1)
    medical_history: Optional[str] = None
    family_history: Optional[str] = None

# 患者响应模式
class PatientResponse(PatientBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 患者列表响应模式
class PatientListResponse(BaseModel):
    items: List[PatientResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        orm_mode = True
