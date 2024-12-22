from typing import override

import pytest
import pytest_asyncio

from app.auth.models import AuthUser, AuthUserNotFoundError
from app.auth.repo import AuthRepo
from app.auth.repo_firebase import AuthRepoFirebase
from app.auth.repo_test import AuthRepoTest
from app.user.models import UserId


class AuthRepoFirebaseTest(AuthRepoTest):
    @override
    @pytest.fixture(scope="module")
    def repo(self) -> AuthRepo:
        return AuthRepoFirebase("test-auth-repo")

    @pytest_asyncio.fixture(autouse=True)  # type: ignore
    async def reset_auth(self, repo: AuthRepo):
        users = ["user_1", "user_2"]
        for id in users:
            try:
                await repo.delete_user(UserId(id))
            except AuthUserNotFoundError:
                continue

    @pytest.mark.asyncio
    async def test_cannot_remove_email_yet(self, repo: AuthRepo, user: AuthUser):
        user.email = None
        await repo.create_user(user)

        user.email = "a@b.c"
        await repo.update_user(user.id, user.model_dump(mode="json"))
        assert await repo.get_user_by_id(user.id) == user

        user.email = None
        await repo.update_user(user.id, user.model_dump(mode="json"))
        user.email = "a@b.c"  # Waiting on https://github.com/firebase/firebase-admin-python/issues/678
        assert await repo.get_user_by_id(user.id) == user
