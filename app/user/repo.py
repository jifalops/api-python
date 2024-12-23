from abc import ABC, abstractmethod
from typing import Any

from app.user.models import FullUser, User, UserId


class UserRepo(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_id(self, id: UserId) -> FullUser:
        raise NotImplementedError()

    @abstractmethod
    async def update_user(self, id: UserId, data: dict[str, Any]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def delete_user(self, id: UserId) -> None:
        raise NotImplementedError()
