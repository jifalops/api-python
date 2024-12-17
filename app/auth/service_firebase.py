import json
import logging
from typing import Any, Optional, override

from firebase_admin import auth, credentials, initialize_app  # type: ignore

from app.auth.service import AuthService
from app.subscription.models import SubscriptionLevel
from app.user.models import Role
from config import (
    FIREBASE_AUTH_EMULATOR_HOST,
    FIREBASE_PROJECT_ID,
    GOOGLE_APPLICATION_CREDENTIALS,
)


class AuthServiceFirebase(AuthService):
    def __init__(self):
        options: dict[str, Any] = {
            "projectId": FIREBASE_PROJECT_ID,
            "httpTimeout": 10,
        }
        if FIREBASE_AUTH_EMULATOR_HOST:
            logging.warning("Using Firebase Auth Emulator")
            initialize_app(options=options)
        else:
            if not GOOGLE_APPLICATION_CREDENTIALS:
                raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not set")
            cred = credentials.Certificate(json.loads(GOOGLE_APPLICATION_CREDENTIALS))
            initialize_app(credential=cred, options=options)

    @override
    async def set_role(self, user_id: str, role: Optional[Role]) -> None:
        await self.set_claims(user_id, {"role": role})

    @override
    async def set_subscription_level(
        self, user_id: str, level: Optional[SubscriptionLevel]
    ) -> None:
        await self.set_claims(user_id, {"level": level})

    @override
    async def is_only_user(self, user_id: str) -> bool:
        page: auth.ListUsersPage = auth.list_users(max_results=2)  # type: ignore
        return len(page.users) == 1 and page.users[0].uid == user_id  # type: ignore

    async def set_claims(self, user_id: str, claims: Optional[dict[str, Any]]) -> None:
        auth.set_custom_user_claims(user_id, claims)  # type: ignore
