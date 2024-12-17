from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import JWT

from app.auth.models import InvalidTokenError, SetRole, UnauthorizedError
from app.auth.service import AuthService
from app.user.models import TokenUser

_security = HTTPBearer()


def decode_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(_security),
) -> TokenUser:
    token = credentials.credentials
    try:
        claims = JWT().decode(token)
    except Exception as e:
        raise InvalidTokenError(exception=e) from e

    return TokenUser(**claims)


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
