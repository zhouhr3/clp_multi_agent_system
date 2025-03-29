"""
API模式包初始化文件，导出所有模式
"""
from .user import *
from .patient import *
from .analysis import *
from .treatment_guideline import *
from .literature import *

# 通用分页查询参数
from pydantic import BaseModel, Field
from typing import Optional

class PaginationParams(BaseModel):
    page: Optional[int] = Field(1, ge=1, description="页码")
    size: Optional[int] = Field(10, ge=1, le=100, description="每页数量")
