from typing import Optional

from app.database.models import Created
from app.service import Service
from app.user.models import FullUser, User
from app.user.repo import UserRepo


class UserService(Service):
    def __init__(self, repo: UserRepo) -> None:
        self._repo = repo

    async def create_user(self, user: User) -> None:
        await self._repo.create_user(user)

    async def get_user(self, user_id: str) -> Created[FullUser]:
        return await self._repo.get_user_by_id(user_id)

    async def set_stripe_customer_id(self, user_id: str, customer_id: str) -> None:
        await self._repo.update_user(user_id, {"stripe_customer_id": customer_id})

    async def set_stripe_subscription_id(
        self, user_id: str, subscription_id: Optional[str]
    ) -> None:
        await self._repo.update_user(
            user_id, {"stripe_subscription_id": subscription_id}
        )
