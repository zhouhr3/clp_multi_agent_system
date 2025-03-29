"""
医学文献模型的API模式定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date

# 医学文献基础模式
class LiteratureBase(BaseModel):
    pubmed_id: str = Field(..., description="PubMed ID，唯一标识")
    title: str = Field(..., description="文献标题")
    authors: List[Dict[str, str]] = Field(..., description="作者信息")
    journal: str = Field(..., description="期刊名称")
    publication_date: date = Field(..., description="发表日期")
    abstract: Optional[str] = Field(None, description="摘要")
    doi: Optional[str] = Field(None, description="DOI链接")
    keywords: Optional[List[str]] = Field(None, description="关键词")

# 医学文献创建请求模式
class LiteratureCreate(LiteratureBase):
    pass

# 医学文献更新请求模式
class LiteratureUpdate(BaseModel):
    title: Optional[str] = Field(None, description="文献标题")
    authors: Optional[List[Dict[str, str]]] = Field(None, description="作者信息")
    journal: Optional[str] = Field(None, description="期刊名称")
    publication_date: Optional[date] = Field(None, description="发表日期")
    abstract: Optional[str] = Field(None, description="摘要")
    doi: Optional[str] = Field(None, description="DOI链接")
    keywords: Optional[List[str]] = Field(None, description="关键词")

# 医学文献响应模式
class LiteratureResponse(LiteratureBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

# 医学文献列表响应模式
class LiteratureListResponse(BaseModel):
    items: List[LiteratureResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        orm_mode = True

# 医学文献搜索请求模式
class LiteratureSearchRequest(BaseModel):
    query: str = Field(..., min_length=2, description="搜索关键词")
    max_results: Optional[int] = Field(10, ge=1, le=100, description="最大结果数")
    page: Optional[int] = Field(1, ge=1, description="页码")
    sort_by: Optional[str] = Field("relevance", description="排序方式: relevance, date")
    date_range: Optional[str] = Field(None, description="日期范围: 1y, 5y, 10y")
