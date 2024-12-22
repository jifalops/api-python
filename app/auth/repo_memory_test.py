from typing import override

import pytest

from app.auth.repo import AuthRepo
from app.auth.repo_memory import AuthRepoMemory
from app.auth.repo_test import AuthRepoTest


class AuthRepoMemoryTest(AuthRepoTest):
    @override
    @pytest.fixture
    def repo(self) -> AuthRepo:
        return AuthRepoMemory()
