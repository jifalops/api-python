from fastapi import APIRouter

from app.auth.models import SignUpData
from app.auth.router import AuthRouter


class AuthRouterFastApi(APIRouter):
    """The FastAPI adapter for the `AuthRouter` port."""

    def __init__(self, router: AuthRouter):
        super().__init__(prefix="/auth", tags=["auth"])
        self._router = router

        self.post("/sign-up")(self.sign_up)

    async def sign_up(self, data: SignUpData) -> str:
        return await self._router.sign_up(data)
