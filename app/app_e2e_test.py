import pytest

from app.app import App
from app.auth.repo_firebase import AuthRepoFirebase
from app.auth.service import AuthService
from app.subscription.service_stripe import SubscriptionServiceStripe
from app.subscription_portal.service_stripe import SubscriptionPortalServiceStripe
from app.user.repo_in_mem import UserRepoInMem
from app.user.service import UserService


@pytest.fixture
def app():
    return App(
        auth=AuthService(repo=AuthRepoFirebase()),
        subscription=SubscriptionServiceStripe(),
        subscription_portal=SubscriptionPortalServiceStripe(),
        user=UserService(repo=UserRepoInMem()),
    )
