from abc import abstractmethod
from datetime import datetime
from typing import Optional

from app.service import Service
from app.subscription.models import SubscriptionLevel
from app.user.models import FullUser, Role, TokenUser


class AuthService(Service):
    """The service that contains the core business logic for authentication."""

    async def sign_up(self, user: TokenUser) -> None:
        await self._app.user.create_user(
            FullUser(
                id=user.id,
                name=user.name,
                email=user.email,
                email_verified=user.email_verified,
                phone=user.phone,
                photo_url=user.photo_url,
                sign_in_methods=[user.sign_in_method],
                created_at=datetime.now(),
            )
        )

    @abstractmethod
    async def set_role(self, user_id: str, role: Optional[Role]) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def set_subscription_level(
        self, user_id: str, level: Optional[SubscriptionLevel]
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def is_only_user(self, user_id: str) -> bool:
        raise NotImplementedError()
