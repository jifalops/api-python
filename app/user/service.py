from app.service import Service
from app.subscription.models import CustomerId, SubscriptionId
from app.user.models import FullUser, User, UserId
from app.user.repo import UserRepo


class UserService(Service):
    def __init__(self, repo: UserRepo) -> None:
        self._repo = repo

    async def create_user(self, user: User) -> None:
        await self._repo.create_user(user)

    async def get_user(self, id: UserId) -> FullUser:
        return await self._repo.get_user_by_id(id)

    async def get_customer(self, id: CustomerId) -> FullUser:
        return await self._repo.get_user_by_customer_id(id)

    async def get_subscriber(self, id: SubscriptionId) -> FullUser:
        return await self._repo.get_user_by_subscription_id(id)

    async def set_customer_id(
        self, user_id: UserId, customer_id: CustomerId | None
    ) -> None:
        await self._repo.update_user(
            user_id,
            {"customer_id": customer_id},
        )

    async def set_subscription_id(
        self, user_id: UserId, subscription_id: SubscriptionId | None
    ) -> None:
        await self._repo.update_user(user_id, {"subscription_id": subscription_id})
