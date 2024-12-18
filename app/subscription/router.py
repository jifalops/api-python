from abc import ABC, abstractmethod

from fastapi import APIRouter, Depends, Request

from app.auth.router import decode_jwt
from app.subscription.models import PortalCreateSubscription, PortalManageBilling
from app.subscription.service import SubscriptionService
from app.user.models import TokenUser


class SubscriptionWebhookHandler(ABC):
    @abstractmethod
    async def handle_webhook(self, request: Request) -> None:
        raise NotImplementedError()


class SubscriptionRouterFastApi(APIRouter):
    def __init__(
        self, service: SubscriptionService, handler: SubscriptionWebhookHandler
    ):
        super().__init__(prefix="/subscription", tags=["subscription"])
        self._service = service

        self.post("/portal/new")(self.create_subscription_with_portal)
        self.post("/portal/edit")(self.create_subscription_with_portal)
        self.post("/webhook")(handler.handle_webhook)

    async def create_subscription_with_portal(
        self, data: PortalCreateSubscription, user: TokenUser = Depends(decode_jwt)
    ):
        return await self._service.create_subscription_with_portal(user, data)

    async def manage_billing_with_portal(
        self, data: PortalManageBilling, user: TokenUser = Depends(decode_jwt)
    ):
        return await self._service.manage_billing_with_portal(user, data)
