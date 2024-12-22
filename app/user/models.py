from typing import NewType

from pydantic import BaseModel

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
