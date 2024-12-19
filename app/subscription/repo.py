from abc import ABC, abstractmethod

from app.subscription.models import Customer, Subscription


class SubscriptionRepo(ABC):
    @abstractmethod
    async def create_customer(self, data: Customer) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_customer_by_id(self, customer_id: str) -> Customer:
        raise NotImplementedError()

    @abstractmethod
    async def get_customer_by_user_id(self, user_id: str) -> Customer:
        raise NotImplementedError()

    @abstractmethod
    async def create_subscription(self, data: Subscription) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get_subscription_by_id(self, subscription_id: str) -> Subscription:
        raise NotImplementedError()

    @abstractmethod
    async def set_subscription_status(self, subscription_id: str, status: str) -> None:
        raise NotImplementedError()
