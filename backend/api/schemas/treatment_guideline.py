"""
治疗指南模型的API模式定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# 治疗指南基础模式
class TreatmentGuidelineBase(BaseModel):
    condition_id: str = Field(..., description="条件ID，如 'non_syndromic_cleft_lip'")
    title: str = Field(..., description="指南标题")
    recommendations: Dict[str, Any] = Field(..., description="治疗建议")
    follow_up: Optional[str] = Field(None, description="随访建议")
    references: Optional[List[str]] = Field(None, description="参考文献")

# 治疗指南创建请求模式
class TreatmentGuidelineCreate(TreatmentGuidelineBase):
    pass

# 治疗指南更新请求模式
class TreatmentGuidelineUpdate(BaseModel):
    title: Optional[str] = Field(None, description="指南标题")
    recommendations: Optional[Dict[str, Any]] = Field(None, description="治疗建议")
    follow_up: Optional[str] = Field(None, description="随访建议")
    references: Optional[List[str]] = Field(None, description="参考文献")

# 治疗指南响应模式
class TreatmentGuidelineResponse(TreatmentGuidelineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# 治疗指南列表响应模式
class TreatmentGuidelineListResponse(BaseModel):
    items: List[TreatmentGuidelineResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        orm_mode = True
