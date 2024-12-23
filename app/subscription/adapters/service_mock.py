from typing import Any, override

from app.subscription.adapters.repo_memory import SubscriptionRepoMemory
from app.subscription.models import PortalCreateSubscription, PortalManageBilling
from app.subscription.service import SubscriptionService
from app.user.models import User


class SubscriptionServiceMock(SubscriptionService):
    def __init__(self):
        self._repo = SubscriptionRepoMemory()

    @override
    async def create_subscription_with_portal(
        self, user: User, data: PortalCreateSubscription
    ) -> str:
        return "http://localhost:8000/subscription/portal/new"

    @override
    async def manage_billing_with_portal(
        self, user: User, data: PortalManageBilling
    ) -> str:
        return "http://localhost:8000/subscription/portal/edit"

    @override
    async def handle_webhook_event(self, event: Any) -> None:
        pass
