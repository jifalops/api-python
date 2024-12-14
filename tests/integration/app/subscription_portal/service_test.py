import os

import pytest

from app.app import App
from app.subscription.models import SubscriptionType
from app.subscription_portal.models import CheckoutStart
from app.user.models import User


@pytest.mark.skipif(
    os.environ.get("CI") == "true" or len(os.environ.get("STRIPE_SECRET_KEY", "")) < 10,
    reason="Requires running dev server running and stripe keys",
)
@pytest.mark.asyncio
async def test_start_checkout_session(app: App):
    info = await app.subscription_portal.start_checkout(
        User(id="1"),
        CheckoutStart(
            type=SubscriptionType(level="plus", period="monthly"),
            success_url="http://localhost:8000/success",
            cancel_url="http://localhost:8000/cancel",
        ),
    )
    assert "http" in info.url
