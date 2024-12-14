import logging
from typing import Optional

import shortuuid

from app.auth.models import SignUpData
from app.service import Service
from app.subscription.models import SubscriptionLevel


class AuthService(Service):
    """The service that contains the core business logic for authentication."""

    async def sign_up(self, data: SignUpData) -> str:
        return f"user_{shortuuid.uuid()}"

    async def set_subscription_level(
        self, user_id: str, level: Optional[SubscriptionLevel]
    ) -> None:
        logging.debug(f"Setting subscription level for user {user_id} to {level}")
        # raise NotImplementedError()
