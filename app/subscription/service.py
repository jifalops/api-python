import asyncio
from abc import abstractmethod
from typing import Optional

from stripe import Subscription

from app.service import Service
from app.subscription.models import (
    PortalCreateSubscription,
    PortalManageBilling,
    SubscriptionPortalSessionLink,
)
from app.user.models import FullUser, User


class SubscriptionService(Service):
    """Core business logic for subscriptions that must be handled by an adapter."""

    async def get_customer_id(self, user: User) -> Optional[str]:
        if not isinstance(user, FullUser):
            user = await self._app.user.get_user(user.id)
        return user.stripe_customer_id

    async def activate_subscription(self, data: Subscription) -> None:
        await asyncio.gather(
            self._app.user.set_subscription(
                user_id,
                subscription_id,
            ),
            self._app.auth.set_subscription_level(user_id, type.level),
        )

    async def deactivate_subscription(self, user_id: str) -> None:
        await asyncio.gather(
            self._repo.set_subscription_id(customer_id, None),
            self._app.auth.set_subscription_level(user_id, None),
        )

    @abstractmethod
    async def create_subscription_with_portal(
        self, user: User, data: PortalCreateSubscription
    ) -> SubscriptionPortalSessionLink:
        raise NotImplementedError()

    @abstractmethod
    async def manage_billing_with_portal(
        self, user: User, data: PortalManageBilling
    ) -> SubscriptionPortalSessionLink:
        raise NotImplementedError()

    @abstractmethod
    async def create_customer(self, user: User) -> str:
        raise NotImplementedError()
