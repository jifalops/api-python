from http import HTTPStatus
from typing import Literal

from pydantic import BaseModel

from app.error import AppError


class Customer(BaseModel):
    id: str
    user_id: str


type SubscriptionLevel = Literal["plus", "pro"]
type SubscriptionPeriod = Literal["monthly", "annual"]
type SubscriptionEdition = Literal["founder"]


class SubscriptionType(BaseModel):
    level: SubscriptionLevel
    period: SubscriptionPeriod
    edition: SubscriptionEdition


class Subscription(BaseModel):
    id: str
    customer_id: str
    type: SubscriptionType
    status: str
    price_id: str


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
