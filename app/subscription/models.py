from http import HTTPStatus
from typing import Literal, NewType

from pydantic import BaseModel

from app.error import AppError
from app.user.models import UserId

CustomerId = NewType("CustomerId", str)
SubscriptionId = NewType("SubscriptionId", str)
PriceId = NewType("PriceId", str)
type SubscriptionLevel = Literal["plus", "pro"]
type SubscriptionPeriod = Literal["monthly", "annual"]
type SubscriptionEdition = Literal["founder"]
__all__ = [
    "CustomerId",
    "SubscriptionId",
    "PriceId",
    "SubscriptionLevel",
    "SubscriptionPeriod",
    "SubscriptionEdition",
]


class SubscriptionType(BaseModel):
    level: SubscriptionLevel
    period: SubscriptionPeriod
    edition: SubscriptionEdition


class Customer(BaseModel):
    id: CustomerId
    user_id: UserId


class Subscription(BaseModel):
    id: SubscriptionId
    customer_id: CustomerId
    price_id: PriceId
    type: SubscriptionType
    status: str

    def is_active(self) -> bool:
        return self.status in ["active", "trialing"]


class PortalCreateSubscription(BaseModel):
    price_id: PriceId
    success_url: str
    cancel_url: str


class PortalManageBilling(BaseModel):
    return_url: str


# Errors


class InvalidWebhookError(AppError):
    def __init__(self, message: str = "Invalid webhook"):
        super().__init__(
            code="subscription/invalid-webhook",
            status=HTTPStatus.BAD_REQUEST,
            message=message,
        )


class InvalidCustomerError(AppError):
    def __init__(self, message: str):
        super().__init__(
            code="subscription/invalid-customer",
            status=HTTPStatus.BAD_REQUEST,
            message=message,
        )


class InvalidPriceError(AppError):
    def __init__(self, message: str):
        super().__init__(
            code="subscription/invalid-price",
            status=HTTPStatus.BAD_REQUEST,
            message=message,
        )


class InvalidProductError(AppError):
    def __init__(self, message: str):
        super().__init__(
            code="subscription/invalid-product",
            status=HTTPStatus.BAD_REQUEST,
            message=message,
        )
