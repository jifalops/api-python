import json
import logging
from typing import Any, override

from stripe import (
    CustomerService,
    Event,
    SignatureVerificationError,
    StripeClient,
    StripeError,
    Webhook,
)

from app.error import AppError
from app.subscription.models import InvalidWebhookError, SubscriptionType
from app.subscription.service import SubscriptionService
from app.user.models import User
from config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET


class SubscriptionServiceStripe(SubscriptionService):
    def __init__(self):
        self.client = StripeClient(STRIPE_SECRET_KEY)

    def is_active(self, status: str) -> bool:
        """https://docs.stripe.com/api/subscriptions/object#subscription_object-status"""
        return status in ["active", "trialing"]

    @override
    async def create_customer_if_necessary(self, user: User) -> str:
        id = await self.get_customer_id(user)
        if id:
            return id

        params = CustomerService.CreateParams(
            metadata={"user_id": user.id},
        )
        if user.name:
            params["name"] = user.name
        if user.email:
            params["email"] = user.email
        if user.phone:
            params["phone"] = user.phone

        try:
            customer = self.client.customers.create(params=params)
        except StripeError as e:
            raise AppError(exception=e)

        await self._app.user.set_stripe_customer_id(user.id, customer.id)
        return customer.id

    @override
    async def handle_webhook(self, headers: dict[str, Any], body: bytes) -> None:
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
                customer = self.client.customers.retrieve(subscription["customer"])
                if customer.metadata and "user_id" in customer.metadata:
                    user_id = customer.metadata["user_id"]
                else:
                    raise AppError("Missing user ID in metadata")

            if self.is_active(subscription["status"]):
                subscription_id = subscription["id"]
                price_id = subscription["items"]["data"][0]["price"]["id"]
                type = self.subscription_type(price_id)
                await self._handle_activation(user_id, subscription_id, type)
            else:
                await self._handle_deactivation(user_id)

    @override
    def type_id(self, type: SubscriptionType) -> str:
        if type.level == "pro" and type.period == "annual":
            return "price_1QVkvZLDlTqaxpeW5OfT8X2n"
        elif type.level == "pro" and type.period == "monthly":
            return "price_1QVkv4LDlTqaxpeWnorpOKQx"
        elif type.level == "plus" and type.period == "annual":
            return "price_1QVkudLDlTqaxpeW47UunUu9"
        elif type.level == "plus" and type.period == "monthly":
            return "price_1QVku7LDlTqaxpeWrLIUGzNt"

        raise ValueError("Invalid subscription type")

    @override
    def subscription_type(self, type_id: str) -> SubscriptionType:
        if type_id == "price_1QVkvZLDlTqaxpeW5OfT8X2n":
            return SubscriptionType(level="pro", period="annual")
        elif type_id == "price_1QVkv4LDlTqaxpeWnorpOKQx":
            return SubscriptionType(level="pro", period="monthly")
        elif type_id == "price_1QVkudLDlTqaxpeW47UunUu9":
            return SubscriptionType(level="plus", period="annual")
        elif type_id == "price_1QVku7LDlTqaxpeWrLIUGzNt":
            return SubscriptionType(level="plus", period="monthly")

        raise ValueError("Invalid price ID")
