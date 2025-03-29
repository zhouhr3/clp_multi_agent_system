from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class Patient(Base):
    """患者模型"""
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    symptoms = Column(ARRAY(String), nullable=False)
    medical_history = Column(Text)
    family_history = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

    # 关系
    creator = relationship("User", back_populates="patients")
    analyses = relationship("Analysis", back_populates="patient", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Patient {self.name}>"
