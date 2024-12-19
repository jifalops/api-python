from typing import override

import stripe
from fastapi import Request
from stripe import Event, SignatureVerificationError, Webhook

from app.error import AppError
from app.subscription.models import InvalidWebhookError
from app.subscription.models import Subscription as AppSubscription
from app.subscription.models import (
    SubscriptionEdition,
    SubscriptionLevel,
    SubscriptionPeriod,
    SubscriptionType,
)
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
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
            "customer.subscription.paused",
            "customer.subscription.resumed",
        ]:
            subscription = event.data.object
            assert subscription["object"] == "subscription"

            if "user_id" in subscription["metadata"]:
                user_id = subscription["metadata"]["user_id"]
            else:
                customer = stripe.Customer.retrieve(subscription["customer"])
                if customer.metadata and "user_id" in customer.metadata:
                    user_id = customer.metadata["user_id"]
                else:
                    raise AppError("Missing user ID in customer metadata")

            if subscription["status"] in ["active", "trialing"]:
                price = subscription["items"]["data"][0]["price"]

                # period
                if price["recurring"]["interval"] == "month":
                    period: SubscriptionPeriod = "monthly"
                elif price["recurring"]["interval"] == "year":
                    period = "annual"
                else:
                    raise AppError("Unknown subscription period recurrence interval")

                # level and edition
                if isinstance(price["product"], str):
                    product = stripe.Product.retrieve(price["product"])
                else:
                    product = price["product"]

                if "level" in product["metadata"]:
                    level: SubscriptionLevel = price["product"]["metadata"]["level"]
                else:
                    raise AppError("Missing subscription level in product metadata")
                if "edition" in product["metadata"]:
                    edition: SubscriptionEdition = price["product"]["metadata"][
                        "edition"
                    ]
                else:
                    raise AppError("Missing subscription edition in product metadata")

                await self._service.activate_subscription(
                    AppSubscription(
                        id=subscription["id"],
                        user_id=user_id,
                        type=SubscriptionType(
                            level=level, period=period, edition=edition
                        ),
                        status=subscription["status"],
                        price_id=price["id"],
                    )
                )
            else:
                await self._service.deactivate_subscription(user_id)
