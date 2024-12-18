import json
import logging
from typing import override

import stripe
from fastapi import Request
from stripe import Event, SignatureVerificationError, Webhook

from app.error import AppError
from app.subscription.models import SUBSCRIPTION_TYPE, InvalidWebhookError
from app.subscription.router import SubscriptionWebhookHandler
from app.subscription.service import SubscriptionService
from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET


class StripeWebhookHandler(SubscriptionWebhookHandler):
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

        if event.type in [
            "checkout.session.completed",
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
        ]:
            subscription = event.data.object
            logging.debug(
                f"Received subscription event: {json.dumps(subscription, indent=2)}"
            )
            try:
                user_id = subscription["metadata"]["user_id"]
            except KeyError:
                # Billing sessions don't have metadata
                customer = stripe.Customer.retrieve(subscription["customer"])
                if customer.metadata and "user_id" in customer.metadata:
                    user_id = customer.metadata["user_id"]
                else:
                    raise AppError("Missing user ID in metadata")

            if subscription["status"] in ["active", "trialing"]:
                subscription_id = subscription["id"]
                price_id = subscription["items"]["data"][0]["price"]["id"]
                type = SUBSCRIPTION_TYPE[price_id]
                await self._service.activate_subscription(
                    user_id, subscription_id, type
                )
            else:
                await self._service.deactivate_subscription(user_id)
