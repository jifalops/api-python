from fastapi import APIRouter, Request

from app.subscription.router import SubscriptionRouter


class SubscriptionRouterFastApi(APIRouter):
    """The FastAPI adapter for the `Subscription` port."""

    def __init__(self, router: SubscriptionRouter):
        super().__init__(prefix="/subscription", tags=["subscription"])
        self._router = router

        self.post("/webhook")(self.webhook)

    async def webhook(self, request: Request) -> None:
        return await self._router.webhook(dict(request.headers), await request.body())
