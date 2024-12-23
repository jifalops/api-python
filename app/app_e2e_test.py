import pytest

from app.app import App
from app.auth.repo_firebase import AuthRepoFirebase
from app.auth.service import AuthService
from app.subscription.adapters.repo_memory import SubscriptionRepoMemory
from app.subscription.adapters.service_stripe import SubscriptionServiceStripe
from app.user.repo_memory import UserRepoMemory
from app.user.service import UserService


@pytest.fixture
def app():
    return App(
        auth=AuthService(repo=AuthRepoFirebase()),
        subscription=SubscriptionServiceStripe(repo=SubscriptionRepoMemory()),
        user=UserService(repo=UserRepoMemory()),
    )
