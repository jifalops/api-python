import asyncio
from abc import abstractmethod

from app.service import Service
from app.subscription.models import (
    PortalCreateSubscription,
    PortalManageBilling,
    Subscription,
    SubscriptionPortalSessionLink,
)
from app.subscription.repo import SubscriptionRepo
from app.user.models import User


class SubscriptionService(Service):
    """Core business logic for subscriptions that must be handled by an adapter."""

    def __init__(self, repo: SubscriptionRepo):
        self._repo = repo

    async def activate_subscription(self, data: Subscription) -> None:
        await asyncio.gather(
            self._app.user.set_subscription_id(
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
