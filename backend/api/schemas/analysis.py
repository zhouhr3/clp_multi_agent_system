"""
分析结果模型的API模式定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# 分析结果基础模式
class AnalysisBase(BaseModel):
    syndrome_type: str = Field(..., description="综合征类型: syndromic 或 non_syndromic")
    syndrome_name: Optional[str] = Field(None, description="如果是综合征性，则记录综合征名称")
    cleft_type: str = Field(..., description="唇腭裂类型，如 '单侧完全性唇裂'")
    severity: str = Field(..., description="严重程度")
    treatment_recommendations: Dict[str, Any] = Field(..., description="治疗建议")
    specialist_recommendations: Optional[Dict[str, Any]] = Field(None, description="专科会诊建议")
    follow_up_plan: Optional[Dict[str, Any]] = Field(None, description="随访计划")

# 分析结果创建请求模式
class AnalysisCreate(AnalysisBase):
    patient_id: int = Field(..., description="患者ID")

# 分析结果更新请求模式
class AnalysisUpdate(BaseModel):
    syndrome_type: Optional[str] = Field(None, description="综合征类型")
    syndrome_name: Optional[str] = Field(None, description="综合征名称")
    cleft_type: Optional[str] = Field(None, description="唇腭裂类型")
    severity: Optional[str] = Field(None, description="严重程度")
    treatment_recommendations: Optional[Dict[str, Any]] = Field(None, description="治疗建议")
    specialist_recommendations: Optional[Dict[str, Any]] = Field(None, description="专科会诊建议")
    follow_up_plan: Optional[Dict[str, Any]] = Field(None, description="随访计划")

# 分析结果响应模式
class AnalysisResponse(AnalysisBase):
    id: int
    patient_id: int
    analyzed_at: datetime
    created_at: datetime

    class Config:
        orm_mode = True

# 分析结果列表响应模式
class AnalysisListResponse(BaseModel):
    items: List[AnalysisResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        orm_mode = True

# 患者分析请求模式
class PatientAnalysisRequest(BaseModel):
    symptoms: List[str] = Field(..., min_items=1, description="症状列表")
    age: str = Field(..., description="患者年龄")
    gender: str = Field(..., description="患者性别")
    medical_history: Optional[str] = Field(None, description="患者病史")
    family_history: Optional[str] = Field(None, description="患者家族史")
