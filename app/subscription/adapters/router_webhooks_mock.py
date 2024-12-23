from typing import override

from fastapi import Request

from app.subscription.router_webhooks import SubscriptionRouterWebhooks


class SubscriptionRouterWebhooksMock(SubscriptionRouterWebhooks):
    @override
    async def handle_webhook(self, request: Request) -> None:
        pass
