from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import JWT

from app.auth.models import SignUpData
from app.auth.service import AuthService
from app.error import AppError
from app.user.models import TokenUser


class AuthRouterFastApi(APIRouter):
    def __init__(self, service: AuthService):
        super().__init__(prefix="/auth", tags=["auth"])
        self._service = service

        self.post("/sign-up")(self.sign_up)

    async def sign_up(self, data: SignUpData) -> str:
        return await self._service.sign_up(data)


_security = HTTPBearer()


def decode_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
) -> TokenUser:
    token = credentials.credentials
    try:
        claims = JWT().decode(token)
    except Exception as e:
        raise AppError(message="Invalid token", exception=e)

    return TokenUser(
        id=claims["sub"],
        sign_in_method=claims.get("sign_in_method", None),
        name=claims.get("name", None),
        email=claims.get("email", None),
        email_verified=claims.get("email_verified", None),
        phone=claims.get("phone_number", None),
        photo_url=claims.get("photo_url", None),
        role=claims.get("role", None),
        level=claims.get("level", None),
    )
