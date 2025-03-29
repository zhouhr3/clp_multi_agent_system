from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class TreatmentGuideline(Base):
    """治疗指南模型"""
    __tablename__ = "treatment_guidelines"

    id = Column(Integer, primary_key=True, index=True)
    condition_id = Column(String, unique=True, index=True, nullable=False)  # 例如：CLP_SYNDROMIC, CL_NONSYNDROMIC
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    cleft_type = Column(String, nullable=False)  # CL, CP, CLP
    syndrome_type = Column(String, nullable=False)  # syndromic, non-syndromic
    age_group = Column(String, nullable=False)  # infant, child, adolescent, adult
    treatment_steps = Column(JSON, nullable=False)
    specialist_involvement = Column(JSON, nullable=False)
    follow_up_protocol = Column(JSON, nullable=False)
    evidence_level = Column(String)  # A, B, C, D
    references = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

    # 关系
    creator = relationship("User", back_populates="guidelines")

    def __repr__(self):
        return f"<TreatmentGuideline {self.condition_id}>"
