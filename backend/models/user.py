from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, default="user")  # user, doctor, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    patients = relationship("Patient", back_populates="creator", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="creator", cascade="all, delete-orphan")
    guidelines = relationship("TreatmentGuideline", back_populates="creator", cascade="all, delete-orphan")
    literatures = relationship("Literature", back_populates="creator", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.email}>"
