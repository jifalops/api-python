from http import HTTPStatus
from typing import NewType

from pydantic import BaseModel

from app.error import AppError

UserId = NewType("UserId", str)
__all__ = ["UserId"]


class User(BaseModel):
    id: UserId
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    avatar: str | None = None

    def is_anonymous(self) -> bool:
        return self.email is None and self.phone is None


class FullUser(User):
    pass


class UserNotFoundError(AppError):
    def __init__(self):
        super().__init__(code="user/not-found", status=HTTPStatus.NOT_FOUND)


class UserAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__(code="user/already-exists", status=HTTPStatus.BAD_REQUEST)


class UserInvalidUpdateError(AppError):
    def __init__(self):
        super().__init__(code="user/invalid-update", status=HTTPStatus.BAD_REQUEST)
