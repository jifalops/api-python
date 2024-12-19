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

    # async def set_stripe_customer_id(self, user_id: str, customer_id: str) -> None:
    #     logging.debug(f"Setting Stripe customer ID for user {user_id} to {customer_id}")
    #     # raise NotImplementedError()

    # async def set_stripe_subscription_id(
    #     self, user_id: str, subscription_id: Optional[str]
    # ) -> None:
    #     logging.debug(
    #         f"Setting subscription ID for user {user_id} to {subscription_id}"
    #     )
    #     # raise NotImplementedError()
