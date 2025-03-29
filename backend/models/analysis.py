from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from .base import Base

class Analysis(Base):
    """分析结果模型"""
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    syndrome_type = Column(String, nullable=False)  # syndromic, non-syndromic
    syndrome_name = Column(String)  # 仅当syndrome_type为syndromic时有值
    cleft_type = Column(String, nullable=False)  # CL, CP, CLP
    severity = Column(String, nullable=False)  # mild, moderate, severe
    treatment_recommendations = Column(JSON, nullable=False)
    specialist_recommendations = Column(JSON)
    follow_up_plan = Column(JSON)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

    # 关系
    patient = relationship("Patient", back_populates="analyses")
    creator = relationship("User", back_populates="analyses")

    def __repr__(self):
        return f"<Analysis {self.id} for Patient {self.patient_id}>"
