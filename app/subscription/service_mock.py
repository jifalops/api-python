from typing import Any, override

from app.subscription.models import SubscriptionType
from app.subscription.service import SubscriptionService
from app.user.models import User


class SubscriptionServiceMock(SubscriptionService):
    @override
    async def create_customer_if_necessary(self, user: User) -> str:
        return user.id

    @override
    async def handle_webhook(self, headers: dict[str, Any], body: bytes) -> None:
        pass

    @override
    def is_active(self, status: str) -> bool:
        return status == "True"

    @override
    def type_id(self, type: SubscriptionType) -> str:
        return f"{type.level}.{type.period}"

    @override
    def subscription_type(self, type_id: str) -> SubscriptionType:
        if "." in type_id:
            level, period = type_id.split(".")
            return SubscriptionType(level=level, period=period)  # type: ignore
        return SubscriptionType(level="pro", period="monthly")
