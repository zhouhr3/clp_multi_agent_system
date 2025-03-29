from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ...models.analysis import Analysis
from ...api.dependencies import get_db
from ...api.schemas.analysis import AnalysisCreate, AnalysisResponse, AnalysisUpdate, AnalysisRequest
from ...utils.auth import get_current_active_user
from ...models.user import User
from ...services.agent_service import analyze_patient_data

router = APIRouter()

@router.get("/", response_model=List[AnalysisResponse])
def get_analyses(
    skip: int = 0, 
    limit: int = 100, 
    patient_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取分析结果列表"""
    query = db.query(Analysis)
    if patient_id:
        query = query.filter(Analysis.patient_id == patient_id)
    analyses = query.offset(skip).limit(limit).all()
    return analyses

@router.post("/", response_model=AnalysisResponse)
def create_analysis(
    analysis_data: AnalysisCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建新分析结果"""
    db_analysis = Analysis(**analysis_data.dict(), created_by=current_user.id)
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_data(
    analysis_request: AnalysisRequest,
    current_user: User = Depends(get_current_active_user)
):
    """分析患者数据（不保存）"""
    # 调用智能体服务进行分析
    analysis_result = await analyze_patient_data(analysis_request.dict())
    return analysis_result

@router.post("/patient/{patient_id}", response_model=AnalysisResponse)
async def analyze_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """分析特定患者并保存结果"""
    # 获取患者数据
    from ...models.patient import Patient
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient is None:
        raise HTTPException(status_code=404, detail="患者不存在")
    
    # 准备分析请求
    analysis_request = {
        "symptoms": patient.symptoms,
        "age": patient.age,
        "gender": patient.gender,
        "medical_history": patient.medical_history,
        "family_history": patient.family_history
    }
    
    # 调用智能体服务进行分析
    analysis_result = await analyze_patient_data(analysis_request)
    
    # 保存分析结果
    db_analysis = Analysis(
        patient_id=patient_id,
        syndrome_type=analysis_result["syndrome_type"],
        syndrome_name=analysis_result.get("syndrome_name"),
        cleft_type=analysis_result["cleft_type"],
        severity=analysis_result["severity"],
        treatment_recommendations=analysis_result["treatment_recommendations"],
        specialist_recommendations=analysis_result.get("specialist_recommendations"),
        follow_up_plan=analysis_result.get("follow_up_plan"),
        created_by=current_user.id
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(
    analysis_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """获取特定分析结果详情"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    return analysis

@router.put("/{analysis_id}", response_model=AnalysisResponse)
def update_analysis(
    analysis_id: int, 
    analysis_data: AnalysisUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新分析结果"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    # 更新分析数据
    for key, value in analysis_data.dict(exclude_unset=True).items():
        setattr(analysis, key, value)
    
    db.commit()
    db.refresh(analysis)
    return analysis

@router.delete("/{analysis_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_analysis(
    analysis_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除分析结果"""
    analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="分析结果不存在")
    
    db.delete(analysis)
    db.commit()
    return None
