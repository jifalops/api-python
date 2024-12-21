from typing import Any, override

from firebase_admin import auth  # type: ignore

from app.auth.models import AuthInvalidUpdateError, AuthUser, UserId
from app.auth.repo import AuthRepo


class AuthRepoFirebase(AuthRepo):
    @override
    async def create_user(self, user: AuthUser) -> None:
        profile = _to_firebase_user(user)
        claims = profile.pop("custom_claims", {})

        auth.create_user(**profile)  # type: ignore
        if len(claims) > 0:
            auth.set_custom_user_claims(user.id, claims)  # type: ignore

    @override
    async def get_user_by_id(self, id: UserId) -> AuthUser:
        user: auth.UserRecord = auth.get_user(id)  # type: ignore
        return _from_firebase_user(user)  # type: ignore

    @override
    async def update_user(self, id: UserId, data: dict[str, Any]) -> None:
        if "id" in data and data["id"] != id:
            raise AuthInvalidUpdateError()

        profile = _to_firebase_user(AuthUser(id=id, **data))
        del profile["uid"]
        claims = profile.pop("custom_claims", {})

        if len(profile) > 0:
            auth.update_user(id, **profile)  # type: ignore
        if len(claims) > 0:
            auth.set_custom_user_claims(id, claims)  # type: ignore

    @override
    async def delete_user(self, id: UserId) -> None:
        return auth.delete_user(id)  # type: ignore

    @override
    async def is_only_user(self, id: UserId) -> bool:
        page: auth.ListUsersPage = auth.list_users(max_results=2)  # type: ignore
        return len(page.users) == 1 and page.users[0].uid == id  # type: ignore


def _from_firebase_user(user: auth.UserRecord) -> AuthUser:
    return AuthUser(
        id=user.uid,  # type: ignore
        name=user.display_name,  # type: ignore
        email=user.email,  # type: ignore
        email_verified=user.email_verified,
        phone=user.phone_number,  # type: ignore
        avatar=user.photo_url,  # type: ignore
        disabled=user.disabled,
        role=(
            None if user.custom_claims is None else user.custom_claims.get("role", None)
        ),
        level=(
            None
            if user.custom_claims is None
            else user.custom_claims.get("level", None)
        ),
    )


def _to_firebase_user(user: AuthUser) -> dict[str, Any]:
    profile: dict[str, Any] = {
        "uid": user.id,
        "display_name": user.name,
        "email": user.email,
        "password": user.password,
        "email_verified": user.email_verified,
        "phone_number": user.phone,
        "photo_url": user.avatar,
        "disabled": user.disabled,
    }

    if user.role is not None or user.level is not None:
        profile["custom_claims"] = {}
        if user.role is not None:
            profile["custom_claims"]["role"] = user.role
        if user.level is not None:
            profile["custom_claims"]["level"] = user.level

    return profile
