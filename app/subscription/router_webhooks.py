from abc import ABC, abstractmethod

from fastapi import Request


class SubscriptionRouterWebhooks(ABC):
    @abstractmethod
    async def handle_webhook(self, request: Request) -> None:
        raise NotImplementedError()
