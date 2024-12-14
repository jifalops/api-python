import pytest

from app.auth.service import AuthService
from app.subscription.service_stripe import SubscriptionServiceStripe
from app.subscription_portal.service_stripe import SubscriptionPortalServiceStripe
from app.user.service import UserService


@pytest.fixture
def app():
    from app.app import App

    return App(
        auth=AuthService(),
        subscription=SubscriptionServiceStripe(),
        subscription_portal=SubscriptionPortalServiceStripe(),
        user=UserService(),
    )
