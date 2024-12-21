from typing import Optional, override

from pydantic import BaseModel

from app.subscription.models import SubscriptionLevel


class User(BaseModel):
    id: str
    name: Optional[str] = None
    email: Optional[str] = None
    email_verified: Optional[bool] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None
    is_disabled: bool = False
    role: Optional[Role] = None
    level: Optional[SubscriptionLevel] = None

    def is_admin(self) -> bool:
        return self.role == "admin"

    def is_subscribed(self) -> bool:
        return self.level is not None

    def to_full_user(self) -> "FullUser":
        return FullUser(
            id=self.id,
            name=self.name,
            email=self.email,
            email_verified=self.email_verified,
            phone=self.phone,
            photo_url=self.photo_url,
            role=self.role,
            level=self.level,
        )


class TokenUser(User):
    sign_in_method: SignInMethod

    @override
    def to_full_user(self) -> "FullUser":
        user = super().to_full_user()
        user.sign_in_methods = [self.sign_in_method]
        return user


class FullUser(User):
    sign_in_methods: list[SignInMethod] = []
    stripe_customer_id: Optional[str] = None
    stripe_subscription_id: Optional[str] = None

    @override
    def to_full_user(self) -> "FullUser":
        return self
