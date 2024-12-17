from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import JWT

from app.auth.models import InvalidTokenError, SetRole, UnauthorizedError
from app.auth.service import AuthService
from app.user.models import TokenUser
from config import VERIFY_TOKEN_SIGNATURE

_security = HTTPBearer()


def decode_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
) -> TokenUser:
    token = credentials.credentials
    try:
        claims = JWT().decode(token, do_verify=VERIFY_TOKEN_SIGNATURE)
    except Exception as e:
        raise InvalidTokenError(exception=e) from e

    return TokenUser(
        id=claims["sub"],
        sign_in_method=claims["firebase"]["sign_in_provider"],
        name=claims.get("name", None),
        email=claims.get("email", None),
        email_verified=claims.get("email_verified", None),
        phone=claims.get("phone_number", None),
        photo_url=claims.get("photo_url", None),
        role=claims.get("role", None),
        level=claims.get("level", None),
    )


class AuthRouter(APIRouter):
    def __init__(self, service: AuthService):
        super().__init__(prefix="/auth", tags=["auth"])
        self._service = service

        self.post("/sign-up")(self.sign_up)
        self.post("/set-role")(self.set_role)

    async def sign_up(self, user: TokenUser = Depends(decode_jwt)) -> None:
        await self._service.sign_up(user)

    async def set_role(
        self, data: SetRole, user: TokenUser = Depends(decode_jwt)
    ) -> None:
        if user.role == "admin" or await self._service.is_only_user(user.id):
            await self._service.set_role(data.user_id, data.role)
        else:
            raise UnauthorizedError()
