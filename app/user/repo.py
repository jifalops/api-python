from abc import ABC, abstractmethod
from typing import Any

from app.database.models import Created
from app.user.models import FullUser, User


class UserRepo(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_id(self, user_id: str) -> Created[FullUser]:
        raise NotImplementedError()

    @abstractmethod
    async def update_user(self, user_id: str, data: dict[str, Any]) -> None:
        raise NotImplementedError()
