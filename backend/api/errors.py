"""
API错误处理模块
"""
from fastapi import HTTPException, status
from typing import Dict, Any, Optional

class APIError(HTTPException):
    """API错误基类"""
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

# 400 错误
class BadRequestError(APIError):
    """400 Bad Request 错误"""
    def __init__(self, detail: str = "无效请求"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

# 401 错误
class UnauthorizedError(APIError):
    """401 Unauthorized 错误"""
    def __init__(self, detail: str = "未授权"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

# 403 错误
class ForbiddenError(APIError):
    """403 Forbidden 错误"""
    def __init__(self, detail: str = "禁止访问"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)

# 404 错误
class NotFoundError(APIError):
    """404 Not Found 错误"""
    def __init__(self, detail: str = "资源不存在"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

# 409 错误
class ConflictError(APIError):
    """409 Conflict 错误"""
    def __init__(self, detail: str = "资源冲突"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)

# 422 错误
class UnprocessableEntityError(APIError):
    """422 Unprocessable Entity 错误"""
    def __init__(self, detail: str = "无法处理的实体"):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)

# 500 错误
class InternalServerError(APIError):
    """500 Internal Server Error 错误"""
    def __init__(self, detail: str = "服务器内部错误"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)
