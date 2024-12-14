from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel

from app.subscription.models import SubscriptionLevel

type Role = Literal["admin", "disabled"]

type SignInMethod = Literal["email_password"]


class User(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    role: Optional[Role] = None
    level: Optional[SubscriptionLevel] = None


class TokenUser(User):
    sign_in_method: SignInMethod


class FullUser(User):
    sign_in_methods: list[SignInMethod]
    created_at: Optional[datetime] = None
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None
