from typing import Any, override

from app.auth.models import (
    AuthInvalidUpdateError,
    AuthUser,
    AuthUserAlreadyExistsError,
    AuthUserNotFoundError,
    UserId,
)
from app.auth.repo import AuthRepo


class AuthRepoMemory(AuthRepo):
    def __init__(self) -> None:
        self._data: dict[UserId, dict[str, Any]] = {}

    @override
    async def create_user(self, user: AuthUser) -> None:
        if user.id in self._data:
            raise AuthUserAlreadyExistsError()
        self._data[user.id] = user.model_dump(mode="json")

    @override
    async def get_user_by_id(self, id: UserId) -> AuthUser:
        if not id in self._data:
            raise AuthUserNotFoundError()
        return AuthUser(**self._data[id])

    @override
    async def update_user(self, id: UserId, data: dict[str, Any]) -> None:
        if "id" in data and data["id"] != id:
            raise AuthInvalidUpdateError()
        if not id in self._data:
            raise AuthUserNotFoundError()
        self._data[id].update(data)

    @override
    async def delete_user(self, id: UserId) -> None:
        if not id in self._data:
            raise AuthUserNotFoundError()
        del self._data[id]

    @override
    async def is_only_user(self, id: UserId) -> bool:
        return len(self._data) == 1 and id in self._data
