from http import HTTPStatus
from typing import Literal, NewType

from pydantic import BaseModel

from app.error import AppError
from app.subscription.models import SubscriptionLevel

UserId = NewType("UserId", str)
type Role = Literal["admin"]


class AuthUser(BaseModel):
    id: UserId
    name: str | None = None
    email: str | None = None
    password: str | None = None
    email_verified: bool = False
    phone: str | None = None
    avatar: str | None = None
    disabled: bool = False
    role: Role | None = None
    level: SubscriptionLevel | None = None

    def is_verified(self) -> bool:
        return self.email_verified or (self.phone != None and len(self.phone) > 0)

    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_subscribed(self) -> bool:
        return self.level is not None


class InvalidTokenError(AppError):
    def __init__(self):
        super().__init__(code="auth/invalid-token", status=HTTPStatus.UNAUTHORIZED)


class UnauthorizedError(AppError):
    def __init__(self):
        super().__init__(code="auth/unauthorized", status=HTTPStatus.UNAUTHORIZED)


class AuthUserNotFoundError(AppError):
    def __init__(self):
        super().__init__(code="auth/user-not-found", status=HTTPStatus.NOT_FOUND)


class AuthUserDisabledError(AppError):
    def __init__(self):
        super().__init__(code="auth/user-disabled", status=HTTPStatus.FORBIDDEN)


class AuthUserAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__(code="auth/user-already-exists", status=HTTPStatus.BAD_REQUEST)


class AuthInvalidUpdateError(AppError):
    def __init__(self):
        super().__init__(code="auth/invalid-update", status=HTTPStatus.BAD_REQUEST)
