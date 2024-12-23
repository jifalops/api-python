import asyncio
from abc import abstractmethod
from typing import Any

from app.error import AppError
from app.service import Service
from app.subscription.models import (
    CustomerId,
    PortalCreateSubscription,
    PortalManageBilling,
    Subscription,
    SubscriptionId,
)
from app.subscription.repo import SubscriptionRepo
from app.user.models import User


class SubscriptionService(Service):
    """Core business logic for subscriptions that must be handled by an adapter."""

    def __init__(self, repo: SubscriptionRepo):
        self._repo = repo

    async def activate_subscription(self, sub: Subscription) -> None:
        customer = await self._repo.get_customer_by_id(sub.customer_id)
        try:
            existing = await self._repo.get_subscription_by_id(sub.id)
        except AppError:
            existing = None

        if existing is None:
            await self._repo.create_subscription(sub)
        else:
            await self._repo.update_subscription(sub.id, sub.model_dump(mode="json"))

        await self._app.auth.set_subscription_level(customer.user_id, sub.type.level)

    async def deactivate_subscription(
        self, subscription_id: SubscriptionId, customer_id: CustomerId, status: str
    ) -> None:
        customer = await self._repo.get_customer_by_id(customer_id)
        await asyncio.gather(
            self._repo.update_subscription(subscription_id, {"status": status}),
            self._app.auth.set_subscription_level(customer.user_id, None),
        )

    @abstractmethod
    async def create_subscription_with_portal(
        self, user: User, data: PortalCreateSubscription
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def manage_billing_with_portal(
        self, user: User, data: PortalManageBilling
    ) -> str:
        raise NotImplementedError()

    @abstractmethod
    async def handle_webhook_event(self, event: Any) -> None:
        raise NotImplementedError()
