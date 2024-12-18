from typing import override

import stripe
from stripe import CustomerService, StripeError
from stripe.checkout import SessionService as CheckoutSessionService

from app.error import AppError
from app.subscription.models import (
    PortalCreateSubscription,
    PortalManageBilling,
    SubscriptionPortalSessionLink,
)
from app.subscription.service import SubscriptionService
from app.user.models import User
from config import STRIPE_SECRET_KEY


class SubscriptionServiceStripe(SubscriptionService):
    def __init__(self):
        stripe.api_key = STRIPE_SECRET_KEY

    @override
    async def create_subscription_with_portal(
        self, user: User, data: PortalCreateSubscription
    ) -> SubscriptionPortalSessionLink:

        customer_id = await self._ensure_customer(user)

        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                metadata={"user_id": user.id},
                mode="subscription",
                line_items=[
                    CheckoutSessionService.CreateParamsLineItem(
                        price=data.price_id,
                        quantity=1,
                    )
                ],
                success_url=data.success_url,
                cancel_url=data.cancel_url,
            )
        except StripeError as e:
            raise AppError(message="Failed to start checkout", exception=e)

        url = session.url
        if not url:
            raise AppError(message="Session has expired.")
        return url

    @override
    async def manage_billing_with_portal(
        self, user: User, data: PortalManageBilling
    ) -> SubscriptionPortalSessionLink:
        customer_id = await self._ensure_customer(user)

        try:
            session = stripe.billing_portal.Session.create(
                customer=customer_id,
                return_url=data.return_url,
            )
        except StripeError as e:
            raise AppError(message="Failed to start billing portal", exception=e)
        return session.url

    @override
    async def create_customer(self, user: User) -> str:
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
            customer = stripe.Customer.create(**params)
        except StripeError as e:
            raise AppError(exception=e)

        await self._app.user.set_stripe_customer_id(user.id, customer.id)
        return customer.id

    async def _ensure_customer(self, user: User) -> str:
        customer_id = await self.get_customer_id(user)
        if not customer_id:
            customer_id = await self.create_customer(user)
        return customer_id
