from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base

class Literature(Base):
    """医学文献模型"""
    __tablename__ = "literatures"

    id = Column(Integer, primary_key=True, index=True)
    pubmed_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    authors = Column(JSON, nullable=False)
    abstract = Column(Text)
    journal = Column(String)
    publication_date = Column(DateTime)
    keywords = Column(JSON)
    cleft_types = Column(JSON)  # 相关的唇腭裂类型
    syndrome_types = Column(JSON)  # 相关的综合征类型
    relevance_score = Column(Integer)  # 相关性评分，1-10
    full_text_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))

    # 关系
    creator = relationship("User", back_populates="literatures")

    def __repr__(self):
        return f"<Literature {self.pubmed_id}>"
