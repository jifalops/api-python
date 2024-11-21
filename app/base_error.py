import logging
from http import HTTPStatus
from typing import Any, Dict, LiteralString, Optional

from fastapi import HTTPException


class BaseError(HTTPException):
    """
    The base error class for the application.

    It extends HTTPException so that an error code is returned to clients if not caught.
    """

    def __init__(
        self,
        code: LiteralString,
        status: HTTPStatus,
        message: Optional[str] = None,
        exception: Optional[Exception] = None,
        context: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status,
            detail=code,
        )

        self.code = code
        """A string in the form `category/error-name`, e.g. `user/not-found`."""

        self.message = message
        self.status = status

        self.exception = exception
        """The exception that caused the error."""

        self.context = context
        """Additional information about the error."""

        # Log the error
        parts = [f"code: {code}"]
        if message:
            parts.append(f"message: {message}")
        if exception:
            parts.append(f"exception: {exception}")
        if context:
            parts.append(f"context: {context}")
        parts.append(f"status={status}")
        logging.error("\n".join(parts))
