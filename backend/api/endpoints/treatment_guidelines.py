from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...models.treatment_guideline import TreatmentGuideline
from ...api.dependencies import get_db
from ...api.schemas.treatment_guideline import TreatmentGuidelineCreate, TreatmentGuidelineResponse, TreatmentGuidelineUpdate
from ...utils.auth import get_current_active_user, get_current_doctor_user
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=List[TreatmentGuidelineResponse])
def get_guidelines(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取治疗指南列表"""
    guidelines = db.query(TreatmentGuideline).offset(skip).limit(limit).all()
    return guidelines

@router.post("/", response_model=TreatmentGuidelineResponse)
def create_guideline(
    guideline_data: TreatmentGuidelineCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor_user)  # 仅医生可创建
):
    """创建新治疗指南"""
    db_guideline = TreatmentGuideline(**guideline_data.dict(), created_by=current_user.id)
    db.add(db_guideline)
    db.commit()
    db.refresh(db_guideline)
    return db_guideline

@router.get("/{condition_id}", response_model=TreatmentGuidelineResponse)
def get_guideline(
    condition_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取特定治疗指南详情"""
    guideline = db.query(TreatmentGuideline).filter(TreatmentGuideline.condition_id == condition_id).first()
    if guideline is None:
        raise HTTPException(status_code=404, detail="治疗指南不存在")
    return guideline

@router.put("/{condition_id}", response_model=TreatmentGuidelineResponse)
def update_guideline(
    condition_id: str, 
    guideline_data: TreatmentGuidelineUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor_user)  # 仅医生可更新
):
    """更新治疗指南"""
    guideline = db.query(TreatmentGuideline).filter(TreatmentGuideline.condition_id == condition_id).first()
    if guideline is None:
        raise HTTPException(status_code=404, detail="治疗指南不存在")
    
    # 更新指南数据
    for key, value in guideline_data.dict(exclude_unset=True).items():
        setattr(guideline, key, value)
    
    db.commit()
    db.refresh(guideline)
    return guideline

@router.delete("/{condition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guideline(
    condition_id: str, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_doctor_user)  # 仅医生可删除
):
    """删除治疗指南"""
    guideline = db.query(TreatmentGuideline).filter(TreatmentGuideline.condition_id == condition_id).first()
    if guideline is None:
        raise HTTPException(status_code=404, detail="治疗指南不存在")
    
    db.delete(guideline)
    db.commit()
    return None
