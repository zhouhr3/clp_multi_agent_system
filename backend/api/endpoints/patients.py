from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...models.patient import Patient
from ...api.dependencies import get_db
from ...api.schemas.patient import PatientCreate, PatientResponse, PatientUpdate
from ...utils.auth import get_current_active_user
from ...models.user import User

router = APIRouter()

@router.get("/", response_model=List[PatientResponse])
def get_patients(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取患者列表"""
    patients = db.query(Patient).offset(skip).limit(limit).all()
    return patients

@router.post("/", response_model=PatientResponse)
def create_patient(
    patient_data: PatientCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建新患者"""
    db_patient = Patient(**patient_data.dict(), created_by=current_user.id)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取特定患者详情"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="患者不存在")
    return patient

@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int, 
    patient_data: PatientUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新患者信息"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    # 更新患者数据
    for key, value in patient_data.dict(exclude_unset=True).items():
        setattr(patient, key, value)
    
    db.commit()
    db.refresh(patient)
    return patient

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(
    patient_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除患者"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    db.delete(patient)
    db.commit()
    return None
