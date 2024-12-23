from typing import override

import stripe
from fastapi import Request
from stripe import Event, SignatureVerificationError, Webhook

from app.subscription.models import InvalidWebhookError
from app.subscription.router_webhooks import SubscriptionRouterWebhooks
from app.subscription.service import SubscriptionService
from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET


class SubscriptionRouterWebhooksStripe(SubscriptionRouterWebhooks):
    def __init__(self, service: SubscriptionService):
        self._service = service
        stripe.api_key = STRIPE_SECRET_KEY

    @override
    async def handle_webhook(self, request: Request) -> None:
        headers = dict(request.headers)
        body = await request.body()
        if not "stripe-signature" in headers:
            raise InvalidWebhookError("Missing signature")

        try:
            event: Event = Webhook.construct_event(  # type: ignore
                sig_header=headers["stripe-signature"],
                payload=body,
                secret=STRIPE_WEBHOOK_SECRET,
            )
        except ValueError:
            raise InvalidWebhookError("Invalid payload")
        except SignatureVerificationError:
            raise InvalidWebhookError("Invalid signature")

        await self._service.handle_webhook_event(event)
