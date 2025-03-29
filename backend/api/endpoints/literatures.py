"""
医学文献API端点
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import List, Optional, Dict, Any
from math import ceil
from datetime import date

from ..schemas.literature import (
    LiteratureCreate, LiteratureUpdate, LiteratureResponse, 
    LiteratureListResponse, LiteratureSearchRequest
)
from ..dependencies import get_current_user, get_current_doctor
from ...models import User, Literature
from ...utils.database import get_db
from ..errors import NotFoundError, ConflictError
from ...services.pubmed_service import search_pubmed, get_pubmed_article

router = APIRouter()

@router.post("", response_model=LiteratureResponse, status_code=status.HTTP_201_CREATED)
async def create_literature(
    literature_in: LiteratureCreate,
    current_user: User = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db)
):
    """
    创建新医学文献记录（仅医生）
    """
    # 检查PubMed ID是否已存在
    result = await db.execute(
        select(Literature).where(Literature.pubmed_id == literature_in.pubmed_id)
    )
    existing_literature = result.scalars().first()
    if existing_literature:
        raise ConflictError(f"PubMed ID {literature_in.pubmed_id} 已存在")
    
    # 创建新医学文献记录
    db_literature = Literature(
        pubmed_id=literature_in.pubmed_id,
        title=literature_in.title,
        authors=literature_in.authors,
        journal=literature_in.journal,
        publication_date=literature_in.publication_date,
        abstract=literature_in.abstract,
        doi=literature_in.doi,
        keywords=literature_in.keywords
    )
    
    db.add(db_literature)
    try:
        await db.commit()
        await db.refresh(db_literature)
        return db_literature
    except IntegrityError:
        await db.rollback()
        raise ConflictError("医学文献记录创建失败，请稍后重试")

@router.get("", response_model=LiteratureListResponse)
async def get_literatures(
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取医学文献列表
    """
    # 构建查询
    query = select(Literature)
    count_query = select(Literature)
    
    # 获取总数
    result = await db.execute(count_query)
    total = len(result.scalars().all())
    
    # 分页查询
    query = query.offset((page - 1) * size).limit(size)
    result = await db.execute(query)
    literatures = result.scalars().all()
    
    # 计算总页数
    pages = ceil(total / size) if total > 0 else 1
    
    return {
        "items": literatures,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }

@router.get("/search", response_model=Dict[str, Any])
async def search_literature(
    query: str = Query(..., min_length=2, description="搜索关键词"),
    max_results: int = Query(10, ge=1, le=100, description="最大结果数"),
    sort_by: str = Query("relevance", description="排序方式: relevance, date"),
    date_range: Optional[str] = Query(None, description="日期范围: 1y, 5y, 10y"),
    current_user: User = Depends(get_current_user)
):
    """
    搜索医学文献
    
    使用PubMed API搜索医学文献，返回搜索结果
    """
    # 使用PubMed API搜索医学文献
    search_results = await search_pubmed(
        query=query,
        max_results=max_results,
        sort_by=sort_by,
        date_range=date_range
    )
    
    return search_results

@router.get("/{pubmed_id}", response_model=LiteratureResponse)
async def get_literature(
    pubmed_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    获取指定医学文献
    
    首先尝试从数据库获取，如果不存在则从PubMed API获取并保存到数据库
    """
    # 从数据库查询医学文献
    result = await db.execute(
        select(Literature).where(Literature.pubmed_id == pubmed_id)
    )
    literature = result.scalars().first()
    
    if literature is None:
        # 从PubMed API获取文献信息
        try:
            article = await get_pubmed_article(pubmed_id)
            
            # 创建新医学文献记录
            literature = Literature(
                pubmed_id=pubmed_id,
                title=article["title"],
                authors=article["authors"],
                journal=article["journal"],
                publication_date=article["publication_date"],
                abstract=article.get("abstract"),
                doi=article.get("doi"),
                keywords=article.get("keywords")
            )
            
            db.add(literature)
            await db.commit()
            await db.refresh(literature)
        except Exception as e:
            raise NotFoundError(f"无法获取PubMed ID {pubmed_id} 的文献信息: {str(e)}")
    
    return literature

@router.put("/{pubmed_id}", response_model=LiteratureResponse)
async def update_literature(
    pubmed_id: str,
    literature_in: LiteratureUpdate,
    current_user: User = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db)
):
    """
    更新指定医学文献（仅医生）
    """
    # 查询医学文献
    result = await db.execute(
        select(Literature).where(Literature.pubmed_id == pubmed_id)
    )
    literature = result.scalars().first()
    
    if literature is None:
        raise NotFoundError(f"PubMed ID {pubmed_id} 不存在")
    
    # 更新医学文献
    if literature_in.title is not None:
        literature.title = literature_in.title
    
    if literature_in.authors is not None:
        literature.authors = literature_in.authors
    
    if literature_in.journal is not None:
        literature.journal = literature_in.journal
    
    if literature_in.publication_date is not None:
        literature.publication_date = literature_in.publication_date
    
    if literature_in.abstract is not None:
        literature.abstract = literature_in.abstract
    
    if literature_in.doi is not None:
        literature.doi = literature_in.doi
    
    if literature_in.keywords is not None:
        literature.keywords = literature_in.keywords
    
    try:
        await db.commit()
        await db.refresh(literature)
        return literature
    except IntegrityError:
        await db.rollback()
        raise ConflictError("医学文献更新失败，请稍后重试")

@router.delete("/{pubmed_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_literature(
    pubmed_id: str,
    current_user: User = Depends(get_current_doctor),
    db: AsyncSession = Depends(get_db)
):
    """
    删除指定医学文献（仅医生）
    """
    # 查询医学文献
    result = await db.execute(
        select(Literature).where(Literature.pubmed_id == pubmed_id)
    )
    literature = result.scalars().first()
    
    if literature is None:
        raise NotFoundError(f"PubMed ID {pubmed_id} 不存在")
    
    await db.delete(literature)
    await db.commit()
    return None
