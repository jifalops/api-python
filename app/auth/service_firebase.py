import json
import logging
from typing import Any

from firebase_admin import credentials, initialize_app  # type: ignore

from app.auth.repo_firebase import AuthRepoFirebase
from app.auth.service import AuthService
from config import (
    FIREBASE_AUTH_EMULATOR_HOST,
    FIREBASE_PROJECT_ID,
    GOOGLE_APPLICATION_CREDENTIALS,
)


class AuthServiceFirebase(AuthService):
    def __init__(self):
        super().__init__(repo=AuthRepoFirebase())

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
