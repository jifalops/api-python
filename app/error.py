import logging
from http import HTTPStatus
from typing import Any, LiteralString


class AppError(Exception):
    """Base exception class for application errors"""

    def __init__(
        self,
        code: LiteralString,
        status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
        message: str | None = None,
        detail: Any = None,
    ):
        super().__init__(f"{code}: {message}")

        self.status = status

        self.code: str = code
        """A string in the form `category/error-name`, e.g. `user/not-found`."""

        self.message: str = message or self.status.phrase
        """A message to be sent along with the error code. Defaults to the [status] phrase."""

        self.detail: Any = detail
        """Additional information about the error that will be logged internally."""

        # Log the error
        parts = [
            f"status: {status}",
            f"code: {code}",
            f"message: {message}",
        ]
        if detail:
            parts.append(f"detail: {detail}")

        logging.error("\n".join(parts))
