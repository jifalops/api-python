from fastapi import APIRouter, Depends

from app.auth.models import AuthUser
from app.auth.router import decode_jwt
from app.subscription.models import PortalCreateSubscription, PortalManageBilling
from app.subscription.router_webhooks import SubscriptionRouterWebhooks
from app.subscription.service import SubscriptionService


class SubscriptionRouter(APIRouter):
    def __init__(
        self, service: SubscriptionService, webhook_handler: SubscriptionRouterWebhooks
    ):
        super().__init__(prefix="/subscription", tags=["subscription"])
        self._service = service

        self.post("/portal/new")(self.create_subscription_with_portal)
        self.post("/portal/edit")(self.create_subscription_with_portal)
        self.post("/webhook")(webhook_handler.handle_webhook)

    async def create_subscription_with_portal(
        self, data: PortalCreateSubscription, user: AuthUser = Depends(decode_jwt)
    ):
        return await self._service.create_subscription_with_portal(user, data)

    async def manage_billing_with_portal(
        self, data: PortalManageBilling, user: AuthUser = Depends(decode_jwt)
    ):
        return await self._service.manage_billing_with_portal(user, data)
