from typing import override

from stripe import StripeClient, StripeError
from stripe.billing_portal import SessionService as BillingPortalSessionService
from stripe.checkout import SessionService as CheckoutSessionService

from app.error import AppError
from app.subscription_portal.models import BillingManage, CheckoutStart, SessionInfo
from app.subscription_portal.service import SubscriptionPortalService
from app.user.models import User
from config import STRIPE_SECRET_KEY


class SubscriptionPortalServiceStripe(SubscriptionPortalService):
    def __init__(self):
        self.client = StripeClient(STRIPE_SECRET_KEY)

    @override
    async def start_checkout(self, user: User, data: CheckoutStart) -> SessionInfo:
        customer_id = await self._app.subscription.create_customer_if_necessary(user)
        params = CheckoutSessionService.CreateParams(
            customer=customer_id,
            metadata={"user_id": user.id},
            mode="subscription",
            line_items=[
                CheckoutSessionService.CreateParamsLineItem(
                    price=self._app.subscription.type_id(data.type),
                    quantity=1,
                )
            ],
            success_url=data.success_url,
            cancel_url=data.cancel_url,
        )

        try:
            session = self.client.checkout.sessions.create(params=params)
        except StripeError as e:
            raise AppError(message="Failed to start checkout", exception=e)

        url = session.url
        if not url:
            raise AppError(message="Session has expired.")
        return SessionInfo(url=url)

    @override
    async def manage_billing(self, user: User, data: BillingManage) -> SessionInfo:
        customer_id = await self._app.subscription.create_customer_if_necessary(user)
        params = BillingPortalSessionService.CreateParams(
            customer=customer_id,
            return_url=data.return_url,
        )
        try:
            session = self.client.billing_portal.sessions.create(params=params)
        except StripeError as e:
            raise AppError(message="Failed to start billing portal", exception=e)
        return SessionInfo(url=session.url)
