from pydantic import BaseModel

from app.subscription.models import SubscriptionType

# Requests


class CheckoutStart(BaseModel):
    type: SubscriptionType
    success_url: str
    cancel_url: str


class BillingManage(BaseModel):
    return_url: str


# Responses


class SessionInfo(BaseModel):
    url: str
