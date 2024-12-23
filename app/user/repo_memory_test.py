from typing import override

import pytest

from app.user.repo import UserRepo
from app.user.repo_memory import UserRepoMemory
from app.user.repo_test import UserRepoTest


class UserRepoMemoryTest(UserRepoTest):
    @override
    @pytest.fixture
    def repo(self) -> UserRepo:
        return UserRepoMemory()
