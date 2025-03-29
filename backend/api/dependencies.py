"""
API依赖项模块，提供API所需的依赖函数
"""
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from ..utils.database import get_db
from ..models import User
from .errors import UnauthorizedError, ForbiddenError
from ..config.settings import settings

# OAuth2 认证方案
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

# 获取当前用户
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    从JWT令牌中获取当前用户
    
    Args:
        token: JWT令牌
        db: 数据库会话
        
    Returns:
        User: 当前用户对象
        
    Raises:
        UnauthorizedError: 如果令牌无效或用户不存在
    """
    try:
        # 解码令牌
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        
        # 获取用户ID
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise UnauthorizedError("无效的认证凭据")
        
        # 获取令牌过期时间
        exp = payload.get("exp")
        if exp is None or datetime.utcnow() > datetime.fromtimestamp(exp):
            raise UnauthorizedError("令牌已过期")
            
    except JWTError:
        raise UnauthorizedError("无效的认证凭据")
    
    # 从数据库获取用户
    user = await db.get(User, user_id)
    if user is None:
        raise UnauthorizedError("用户不存在")
    
    # 检查用户是否激活
    if not user.is_active:
        raise ForbiddenError("用户已被禁用")
        
    return user

# 获取当前活跃用户
async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户对象
        
    Returns:
        User: 当前活跃用户对象
        
    Raises:
        ForbiddenError: 如果用户未激活
    """
    if not current_user.is_active:
        raise ForbiddenError("用户已被禁用")
    return current_user

# 获取当前超级用户
async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前超级用户
    
    Args:
        current_user: 当前用户对象
        
    Returns:
        User: 当前超级用户对象
        
    Raises:
        ForbiddenError: 如果用户不是超级用户
    """
    if not current_user.is_superuser:
        raise ForbiddenError("需要管理员权限")
    return current_user

# 获取当前医生用户
async def get_current_doctor(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前医生用户
    
    Args:
        current_user: 当前用户对象
        
    Returns:
        User: 当前医生用户对象
        
    Raises:
        ForbiddenError: 如果用户不是医生
    """
    if current_user.role != "doctor" and not current_user.is_superuser:
        raise ForbiddenError("需要医生权限")
    return current_user

# 创建访问令牌
def create_access_token(
    data: Dict[str, Any], 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建JWT访问令牌
    
    Args:
        data: 令牌数据
        expires_delta: 过期时间增量
        
    Returns:
        str: JWT令牌
    """
    to_encode = data.copy()
    
    # 设置过期时间
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    # 编码令牌
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    
    return encoded_jwt
