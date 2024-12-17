import logging
from datetime import datetime
from typing import Optional

from app.service import Service
from app.user.models import FullUser


class UserService(Service):
    async def create_user(self, user: FullUser) -> None:
        logging.warning(f"Creating user {user.id}")
        # raise NotImplementedError()

    async def get_user(self, user_id: str) -> FullUser:
        logging.warning(f"Returning fake user")
        return FullUser(
            id=user_id,
            created_at=datetime.now(),
            sign_in_methods=["email_password"],
        )
        # raise NotImplementedError()

    async def set_stripe_customer_id(self, user_id: str, customer_id: str) -> None:
        logging.debug(f"Setting Stripe customer ID for user {user_id} to {customer_id}")
        # raise NotImplementedError()

    async def set_stripe_subscription_id(
        self, user_id: str, subscription_id: Optional[str]
    ) -> None:
        logging.debug(
            f"Setting subscription ID for user {user_id} to {subscription_id}"
        )
        # raise NotImplementedError()
