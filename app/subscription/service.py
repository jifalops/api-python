import asyncio
from abc import abstractmethod
from typing import Any

from app.service import Service
from app.subscription.models import CustomerId, SubscriptionId, SubscriptionType
from app.subscription.repo import SubscriptionRepo
from app.user.models import User, UserId


class SubscriptionService(Service):
    def __init__(self, repo: SubscriptionRepo):
        self._repo = repo

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

    async def _handle_activation(
        self, user_id: UserId, subscription_id: SubscriptionId, type: SubscriptionType
    ) -> None:
        await asyncio.gather(
            self._repo.set_subscription_id(user_id, subscription_id),
            self._app.auth.set_subscription_level(user_id, type.level),
        )

    async def _handle_deactivation(
        self, user_id: UserId, customer_id: CustomerId
    ) -> None:
        await asyncio.gather(
            self._repo.set_subscription_id(customer_id, None),
            self._app.auth.set_subscription_level(user_id, None),
        )
