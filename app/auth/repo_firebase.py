import json
import logging
import os
from typing import Any, override

from firebase_admin import auth, credentials, initialize_app  # type: ignore

from app.auth.models import AuthInvalidUpdateError, AuthUser
from app.auth.repo import AuthRepo
from app.user.models import UserAlreadyExistsError, UserId, UserNotFoundError
from config import FIREBASE_PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS


class AuthRepoFirebase(AuthRepo):
    def __init__(self, project_id: str = FIREBASE_PROJECT_ID) -> None:
        options: dict[str, Any] = {
            "projectId": project_id,
            "httpTimeout": 10,
        }
        if os.environ.get("FIREBASE_AUTH_EMULATOR_HOST", ""):
            # Firebase Auth checks for that environment variable.
            logging.warning("Using Firebase Auth Emulator")
            initialize_app(options=options)
        else:
            if not GOOGLE_APPLICATION_CREDENTIALS:
                raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")
            cred = credentials.Certificate(json.loads(GOOGLE_APPLICATION_CREDENTIALS))
            initialize_app(credential=cred, options=options)

    @override
    async def create_user(self, user: AuthUser) -> None:
        profile = _to_firebase_user(user)
        claims = profile.pop("custom_claims", {})

        try:
            auth.create_user(**profile)  # pyright: ignore[reportUnknownMemberType]
        except auth.UidAlreadyExistsError as e:
            raise UserAlreadyExistsError() from e
        if len(claims) > 0:
            try:
                auth.set_custom_user_claims(  # pyright: ignore[reportUnknownMemberType]
                    user.id,
                    claims,
                )
            except auth.UserNotFoundError as e:
                raise UserNotFoundError() from e

    @override
    async def get_user_by_id(self, id: UserId) -> AuthUser:
        try:
            user: auth.UserRecord = auth.get_user(id)  # type: ignore
        except auth.UserNotFoundError as e:
            raise UserNotFoundError() from e
        return _from_firebase_user(user)  # type: ignore

    @override
    async def update_user(self, id: UserId, data: dict[str, Any]) -> None:
        if "id" in data and data["id"] != id:
            raise AuthInvalidUpdateError()

        profile = _to_firebase_user(AuthUser(**data))
        del profile["uid"]
        claims = profile.pop("custom_claims", {})

        for key, value in profile.items():
            if value is None and key in ["display_name", "phone_number", "photo_url"]:
                profile[key] = auth.DELETE_ATTRIBUTE

        if len(profile) > 0:
            try:
                auth.update_user(id, **profile)  # type: ignore
            except auth.UserNotFoundError as e:
                raise UserNotFoundError() from e
        if len(claims) > 0:
            try:
                auth.set_custom_user_claims(id, claims)  # type: ignore
            except auth.UserNotFoundError as e:
                raise UserNotFoundError() from e

    @override
    async def delete_user(self, id: UserId) -> None:
        try:
            return auth.delete_user(id)  # type: ignore
        except auth.UserNotFoundError as e:
            raise UserNotFoundError() from e

    @override
    async def is_only_user(self, id: UserId) -> bool:
        page: auth.ListUsersPage = auth.list_users(max_results=2)  # type: ignore
        return len(page.users) == 1 and page.users[0].uid == id  # type: ignore


def _from_firebase_user(user: auth.UserRecord) -> AuthUser:
    logging.debug(f"Translating Firebase user: {user}")
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

    profile["custom_claims"] = {}
    if user.role is not None:
        profile["custom_claims"]["role"] = user.role
    if user.level is not None:
        profile["custom_claims"]["level"] = user.level

    return profile
