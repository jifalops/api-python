import shortuuid

from app.auth.models import SignUpData
from app.base_service import BaseService


class AuthService(BaseService):
    """The service that contains the core business logic for authentication."""

    async def sign_up(self, data: SignUpData) -> str:
        return f"user_{shortuuid.uuid()}"
