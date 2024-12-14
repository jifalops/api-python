import logging
from http import HTTPStatus
from typing import LiteralString, Optional


class AppError(Exception):
    """Base exception class for application errors"""

    def __init__(
        self,
        code: LiteralString = "error/internal",
        status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR,
        message: Optional[str] = None,
        exception: Optional[Exception] = None,
        details: Optional[dict[str, object]] = None,
    ):
        super().__init__(f"{code}: {message}")

        self.code: str = code
        """A string in the form `category/error-name`, e.g. `user/not-found`."""

        self.message = message
        self.status = status

        self.details = details
        """Additional information about the error."""

        # Log the error
        parts = [f"code: {code}"]
        if message:
            parts.append(f"message: {message}")
        if exception:
            parts.append(f"exception: {exception}")
        if details:
            parts.append(f"details: {details}")
        parts.append(f"status={status}")
        logging.error("\n".join(parts))
