from dataclasses import dataclass
from typing import List

from app.auth.service import AuthService
from app.base_service import BaseService


@dataclass
class App:
    """
    The container for services that the application uses.

    Each entry point (main.py, testing, etc.) creates an `App` instance with the appropriate configuration.
    """

    auth: AuthService

    def __post_init__(self):
        self._services: List[BaseService] = [
            self.auth,
        ]
        for service in self._services:
            service._set_app(self)  # type: ignore

    async def shutdown(self):
        for service in self._services:
            await service.destroy()
