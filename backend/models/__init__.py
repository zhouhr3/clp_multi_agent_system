"""
模型包初始化文件，导出所有模型
"""
from .base import BaseModel
from .user import User
from .patient import Patient
from .analysis import Analysis
from .treatment_guideline import TreatmentGuideline
from .literature import Literature

# 导出所有模型，方便导入
__all__ = [
    "BaseModel",
    "User",
    "Patient",
    "Analysis",
    "TreatmentGuideline",
    "Literature"
]
