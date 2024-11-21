from app.auth.models import SignUpData
from app.auth.service import AuthService


class AuthRouter:
    """The driving port for authentication."""

    def __init__(self, service: AuthService):
        self.service = service

    async def sign_up(self, data: SignUpData) -> str:
        return await self.service.sign_up(data)
