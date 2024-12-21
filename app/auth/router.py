import jwt
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.models import AuthUser, InvalidTokenError, Role, UnauthorizedError, UserId
from app.auth.service import AuthService
from config import VERIFY_TOKEN_SIGNATURE

_security = HTTPBearer()


def decode_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
) -> AuthUser:
    token = credentials.credentials
    try:
        claims = jwt.decode(token, do_verify=VERIFY_TOKEN_SIGNATURE)
    except Exception as e:
        raise InvalidTokenError() from e

    return AuthUser(
        id=claims["sub"],
        role=claims.get("role", None),
        level=claims.get("level", None),
    )


class AuthRouter(APIRouter):
    def __init__(self, service: AuthService):
        super().__init__(prefix="/auth", tags=["auth"])
        self._service = service

        self.post("/sign-up")(self.sign_up)
        self.post("/set-role")(self.set_role)

    async def sign_up(self, user: AuthUser = Depends(decode_jwt)) -> None:
        await self._service.sign_up(user)

    async def set_role(
        self, user_id: UserId, role: Role, user: AuthUser = Depends(decode_jwt)
    ) -> None:
        if user.role == "admin" or await self._service.is_only_user(user.id):
            await self._service.set_role(user_id, role)
        else:
            raise UnauthorizedError()
