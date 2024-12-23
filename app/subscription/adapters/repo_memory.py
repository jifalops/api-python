from typing import Any, override

from app.error import AppError
from app.subscription.models import Customer, CustomerId, Subscription, SubscriptionId
from app.subscription.repo import SubscriptionRepo
from app.user.models import UserId


class SubscriptionRepoMemory(SubscriptionRepo):
    def __init__(self):
        self._cust: dict[CustomerId, dict[str, Any]] = {}
        self._sub: dict[SubscriptionId, dict[str, Any]] = {}

    @override
    async def create_customer(self, data: Customer) -> None:
        if data.id in self._cust:
            raise AppError("subscription/customer-exists")
        self._cust[data.id] = data.model_dump(mode="json")

    @override
    async def get_customer_by_id(self, id: CustomerId) -> Customer:
        if not id in self._cust:
            raise AppError("subscription/customer-not-found")
        return Customer(**self._cust[id])

    @override
    async def get_customer_by_user_id(self, id: UserId) -> Customer:
        for value in self._cust.values():
            if value.get("user_id", None) == id:
                return Customer(**value)
        raise AppError("subscription/customer-not-found")

    @override
    async def create_subscription(self, data: Subscription) -> None:
        if data.id in self._sub:
            raise AppError("subscription/subscription-exists")
        self._sub[data.id] = data.model_dump(mode="json")

    @override
    async def get_subscription_by_id(self, id: SubscriptionId) -> Subscription:
        if not id in self._sub:
            raise AppError("subscription/subscription-not-found")
        return Subscription(**self._sub[id])

    @override
    async def update_subscription(
        self, id: SubscriptionId, data: dict[str, Any]
    ) -> None:
        if "id" in data and data["id"] != id:
            raise AppError("subscription/invalid-update")
        if not id in self._sub:
            raise AppError("subscription/subscription-not-found")
        self._sub[id].update(data)
