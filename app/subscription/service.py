import asyncio
from abc import abstractmethod
from typing import Any, Optional

from app.service import Service
from app.subscription.models import SubscriptionType
from app.user.models import User


class SubscriptionService(Service):

    @abstractmethod
    async def create_customer_if_necessary(self, user: User) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def handle_webhook(self, headers: dict[str, Any], body: bytes) -> None:
        raise NotImplementedError()

    @abstractmethod
    def is_active(self, status: str) -> bool:
        raise NotImplementedError()

    @abstractmethod
    def type_id(self, type: SubscriptionType) -> str:
        raise NotImplementedError()

    @abstractmethod
    def subscription_type(self, type_id: str) -> SubscriptionType:
        raise NotImplementedError()

    async def get_customer_id(self, user: User) -> Optional[str]:
        if not isinstance(user, User):
            user = await self._app.user.get_user(user.id)

        return user.stripe_customer_id

    async def _handle_activation(
        self, user_id: str, subscription_id: str, type: SubscriptionType
    ) -> None:
        await asyncio.gather(
            self._app.user.set_stripe_subscription_id(user_id, subscription_id),
            self._app.auth.set_subscription_level(user_id, type.level),
        )

    async def _handle_deactivation(self, user_id: str) -> None:
        await asyncio.gather(
            self._app.user.set_stripe_subscription_id(user_id, None),
            self._app.auth.set_subscription_level(user_id, None),
        )
