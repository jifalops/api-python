from http import HTTPStatus
from typing import Literal

from pydantic import BaseModel

from app.error import AppError

type SubscriptionLevel = Literal["plus", "pro"]
type SubscriptionPeriod = Literal["monthly", "annual"]


class SubscriptionType(BaseModel):
    level: SubscriptionLevel
    period: SubscriptionPeriod


class InvalidWebhookError(AppError):
    def __init__(self, message: str = "Invalid webhook request"):
        super().__init__(
            code="webhook/invalid",
            status=HTTPStatus.BAD_REQUEST,
            message=message,
        )
