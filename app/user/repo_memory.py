from typing import Any, override

from app.user.models import (
    FullUser,
    User,
    UserAlreadyExistsError,
    UserId,
    UserInvalidUpdateError,
    UserNotFoundError,
)
from app.user.repo import UserRepo


class UserRepoMemory(UserRepo):
    def __init__(self):
        self._data: dict[UserId, dict[str, Any]] = {}

    @override
    async def create_user(self, user: User) -> None:
        if user.id in self._data:
            raise UserAlreadyExistsError()
        self._data[user.id] = user.model_dump(mode="json")

    @override
    async def get_user_by_id(self, id: UserId) -> FullUser:
        if not id in self._data:
            raise UserNotFoundError()
        return FullUser(**self._data[id])

    @override
    async def update_user(self, id: UserId, data: dict[str, Any]) -> None:
        if "id" in data and data["id"] != id:
            raise UserInvalidUpdateError()
        if not id in self._data:
            raise UserNotFoundError()
        self._data[id].update(data)

    @override
    async def delete_user(self, id: UserId) -> None:
        if not id in self._data:
            raise UserNotFoundError()
        del self._data[id]
