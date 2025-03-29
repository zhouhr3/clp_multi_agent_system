"""
安全工具模块，提供密码哈希和验证功能
"""
from passlib.context import CryptContext
import secrets
import string

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    获取密码哈希
    
    Args:
        password: 原始密码
        
    Returns:
        str: 密码哈希
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码
    
    Args:
        plain_password: 原始密码
        hashed_password: 密码哈希
        
    Returns:
        bool: 密码是否匹配
    """
    return pwd_context.verify(plain_password, hashed_password)

def generate_random_password(length: int = 12) -> str:
    """
    生成随机密码
    
    Args:
        length: 密码长度
        
    Returns:
        str: 随机密码
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))
