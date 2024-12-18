from datetime import datetime
from http import HTTPStatus
from typing import Literal, NewType

from pydantic import BaseModel

from app.error import AppError
from app.user.models import UserId

CustomerId = NewType("CustomerId", str)
SubscriptionId = NewType("SubscriptionId", str)
type SubscriptionLevel = Literal["plus", "pro"]
type SubscriptionPeriod = Literal["monthly", "annual"]
__all__ = ["CustomerId", "SubscriptionId", "SubscriptionLevel", "SubscriptionPeriod"]


class Customer(BaseModel):
    id: CustomerId
    user_id: UserId


class SubscriptionType(BaseModel):
    level: SubscriptionLevel
    period: SubscriptionPeriod


class Subscription(BaseModel):
    id: str
    user_id: str
    type: SubscriptionType
    status: str
    price_id: str
    created_at: datetime


class PortalCreateSubscription(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str


class PortalManageBilling(BaseModel):
    return_url: str


type SubscriptionPortalSessionLink = str


# Errors


class InvalidWebhookError(AppError):
    def __init__(self, message: str = "Invalid webhook request"):
        super().__init__(
            code="webhook/invalid",
            status=HTTPStatus.BAD_REQUEST,
            message=message,
        )
