import os
from datetime import timedelta
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ...models.user import User
from ...api.dependencies import get_db
from ...api.schemas.user import UserCreate, UserResponse, UserUpdate, Token
from ...utils.auth import authenticate_user, create_access_token, get_password_hash, get_current_active_user
from ...config.settings import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """注册新用户"""
    # 检查邮箱是否已存在
    db_user = db.query(User).filter(User.email == user_data.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role="user"  # 默认角色为普通用户
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录获取访问令牌"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码不正确",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """获取当前用户信息"""
    return current_user

@router.put("/me", response_model=UserResponse)
def update_user_me(user_data: UserUpdate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """更新当前用户信息"""
    # 更新用户信息
    if user_data.full_name is not None:
        current_user.full_name = user_data.full_name
    
    if user_data.email is not None and user_data.email != current_user.email:
        # 检查新邮箱是否已存在
        db_user = db.query(User).filter(User.email == user_data.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被注册"
            )
        current_user.email = user_data.email
    
    if user_data.password is not None:
        current_user.hashed_password = get_password_hash(user_data.password)
    
    db.commit()
    db.refresh(current_user)
    return current_user
