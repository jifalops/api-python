from typing import override

import stripe
from stripe import CustomerService, Event, StripeError
from stripe.checkout import SessionService as CheckoutSessionService

from app.error import AppError
from app.subscription.models import Customer as AppCustomer
from app.subscription.models import (
    CustomerId,
    InvalidPriceError,
    InvalidProductError,
    PortalCreateSubscription,
    PortalManageBilling,
    PriceId,
)
from app.subscription.models import Subscription as AppSubscription
from app.subscription.models import (
    SubscriptionEdition,
    SubscriptionId,
    SubscriptionLevel,
    SubscriptionPeriod,
    SubscriptionType,
)
from app.subscription.repo import SubscriptionRepo
from app.subscription.service import SubscriptionService
from app.user.models import User
from config import STRIPE_SECRET_KEY


class SubscriptionServiceStripe(SubscriptionService):
    def __init__(self, repo: SubscriptionRepo):
        self._repo = repo
        stripe.api_key = STRIPE_SECRET_KEY

    @override
    async def create_subscription_with_portal(
        self, user: User, data: PortalCreateSubscription
    ) -> str:
        customer = await self.get_or_create_customer(user)

        try:
            session = stripe.checkout.Session.create(
                customer=customer.id,
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
            raise AppError(
                code="subscription/checkout-session",
                message="Failed to start session",
            ) from e

        url = session.url
        if not url:
            raise AppError(
                code="subscription/checkout-session",
                message="Session expired",
            )
        return url

    @override
    async def manage_billing_with_portal(
        self, user: User, data: PortalManageBilling
    ) -> str:
        customer = await self.get_or_create_customer(user)

        try:
            session = stripe.billing_portal.Session.create(
                customer=customer.id,
                return_url=data.return_url,
            )
        except StripeError as e:
            raise AppError(
                code="subscription/billing-session",
                message="Failed to start session",
            ) from e
        return session.url

    async def get_or_create_customer(self, user: User) -> AppCustomer:
        try:
            return await self._repo.get_customer_by_user_id(user.id)
        except AppError:
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
                raise AppError(code="subcription/create-customer") from e

            app_customer = AppCustomer(id=CustomerId(customer.id), user_id=user.id)

            await self._repo.create_customer(app_customer)  # TODO retry
            return app_customer

    @override
    async def handle_webhook_event(self, event: Event) -> None:
        if event.type in [
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
            "customer.subscription.paused",
            "customer.subscription.resumed",
        ]:
            assert event.data.object == "subscription"
            subscription = event.data.object

            subscription_id = SubscriptionId(subscription["id"])
            customer_id = CustomerId(subscription["customer"])

            # Active subscription
            if subscription["status"] in ["active", "trialing"]:
                price = subscription["items"]["data"][0]["price"]

                # Subscription period/interval
                if price["recurring"]["interval"] == "month":
                    period: SubscriptionPeriod = "monthly"
                elif price["recurring"]["interval"] == "year":
                    period = "annual"
                else:
                    raise InvalidPriceError("Unknown interval")

                # Fetch product if necessary
                if isinstance(price["product"], str):
                    product = stripe.Product.retrieve(price["product"])
                else:
                    product = price["product"]

                # Subscription level/tier
                if "level" in product["metadata"]:
                    level: SubscriptionLevel = price["product"]["metadata"]["level"]
                else:
                    raise InvalidProductError("Missing subscription level")

                # Subscription edition
                if "edition" in product["metadata"]:
                    edition: SubscriptionEdition = price["product"]["metadata"][
                        "edition"
                    ]
                else:
                    raise InvalidProductError("Missing subscription edition")

                await self.activate_subscription(
                    AppSubscription(
                        id=subscription_id,
                        customer_id=customer_id,
                        price_id=PriceId(price["id"]),
                        type=SubscriptionType(
                            level=level, period=period, edition=edition
                        ),
                        status=subscription["status"],
                    )
                )
            else:
                await self.deactivate_subscription(
                    subscription_id, customer_id, subscription["status"]
                )
