from http import HTTPStatus
from typing import Any, Optional

from pydantic import BaseModel

from app.error import AppError
from app.user.models import Role


class SetRole(BaseModel):
    user_id: str
    role: Optional[Role]


class InvalidTokenError(AppError):
    def __init__(self, exception: Exception, details: Optional[dict[str, Any]] = None):
        super().__init__(
            code="auth/invalid-token",
            message="Invalid token",
            status=HTTPStatus.UNAUTHORIZED,
            exception=exception,
            details=details,
        )


class UnauthorizedError(AppError):
    def __init__(self, details: Optional[dict[str, Any]] = None):
        super().__init__(
            code="auth/unauthorized",
            message="Unauthorized",
            status=HTTPStatus.UNAUTHORIZED,
            details=details,
        )
