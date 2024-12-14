from typing import Any

from app.subscription.service import SubscriptionService


class SubscriptionRouter:
    """The driving port for subscriptions."""

    def __init__(self, service: SubscriptionService):
        self.service = service

    async def webhook(self, headers: dict[str, Any], body: bytes) -> None:
        await self.service.handle_webhook(headers=headers, body=body)
