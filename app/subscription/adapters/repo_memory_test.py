from typing import override

import pytest

from app.subscription.adapters.repo_memory import SubscriptionRepoMemory
from app.subscription.repo import SubscriptionRepo
from app.subscription.repo_test import SubscriptionRepoTest


class SubscriptionRepoMemoryTest(SubscriptionRepoTest):
    @override
    @pytest.fixture
    def repo(self) -> SubscriptionRepo:
        return SubscriptionRepoMemory()
