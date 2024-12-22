from abc import ABC, abstractmethod
from typing import Any

from app.auth.models import AuthUser
from app.user.models import UserId


class AuthRepo(ABC):
    @abstractmethod
    async def create_user(self, user: AuthUser) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_id(self, id: UserId) -> AuthUser:
        raise NotImplementedError()

    @abstractmethod
    async def update_user(self, id: UserId, data: dict[str, Any]) -> None:
        """
        Update the properties on a user.

        Only the properties that are provided will be changed.
        To remove a property, set its value to None.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_user(self, id: UserId) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def is_only_user(self, id: UserId) -> bool:
        raise NotImplementedError()
