from abc import ABC, abstractmethod
from typing import Any

from app.subscription.models import Customer, CustomerId, Subscription, SubscriptionId
from app.user.models import UserId


class SubscriptionRepo(ABC):
    @abstractmethod
    async def create_customer(self, data: Customer) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_customer_by_id(self, id: CustomerId) -> Customer:
        raise NotImplementedError()

    @abstractmethod
    async def get_customer_by_user_id(self, id: UserId) -> Customer:
        raise NotImplementedError()

    @abstractmethod
    async def create_subscription(self, data: Subscription) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_subscription_by_id(self, id: SubscriptionId) -> Subscription:
        raise NotImplementedError()

    @abstractmethod
    async def update_subscription(
        self, id: SubscriptionId, data: dict[str, Any]
    ) -> None:
        raise NotImplementedError()
