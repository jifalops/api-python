from app.auth.models import AuthUser, Role, UserId
from app.auth.repo import AuthRepo
from app.service import Service
from app.subscription.models import SubscriptionLevel


class AuthService(Service):
    """Business logic around authentication and authorization."""

    def __init__(self, repo: AuthRepo):
        self._repo = repo

    async def sign_up(self, user: AuthUser) -> None:
        await self._repo.create_user(user)

    async def get_user(self, id: UserId) -> AuthUser:
        return await self._repo.get_user_by_id(id)

    async def set_role(self, id: UserId, role: Role):
        await self._repo.update_user(id, {"role": role})

    async def is_only_user(self, id: UserId) -> bool:
        """
        Check if the user is the only user in the system.

        This is useful for bootstrapping the first admin user.
        """
        return await self._repo.is_only_user(id)

    async def disable_user(self, id: UserId):
        await self._repo.update_user(id, {"disabled": True})

    async def set_subscription_level(self, id: UserId, level: SubscriptionLevel):
        await self._repo.update_user(id, {"level": level})

    async def delete_user(self, id: UserId):
        await self._repo.delete_user(id)
