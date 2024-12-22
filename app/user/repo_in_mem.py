from datetime import datetime
from typing import Any, override

from app.database.models import Created
from app.user.models import FullUser, User
from app.user.repo import UserRepo


class UserRepoInMem(UserRepo):
    def __init__(self):
        self._data: dict[str, Any] = {}

    @override
    async def create_user(self, user: User) -> None:
        if user.id in self._data:
            raise ValueError(f"User {user.id} already exists.")
        self._data[user.id] = Created[FullUser](
            created_at=datetime.now(),
            model=user.to_full_user(),
        )

    @override
    async def get_user_by_id(self, user_id: str) -> Created[FullUser]:
        if user_id not in self._data:
            raise ValueError(f"User {user_id} does not exist.")
        return self._data[user_id]

    @override
    async def update_user(self, user_id: str, data: dict[str, Any]) -> None:
        if user_id not in self._data:
            raise ValueError(f"User {user_id} does not exist.")
        self._data[user_id].update(data)
