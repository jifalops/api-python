from dataclasses import dataclass

from app.auth.service import AuthService
from app.service import Service
from app.subscription.service import SubscriptionService
from app.user.service import UserService


@dataclass
class App:
    """
    The container for services that the application uses.

    Each entry point (main.py, testing, etc.) creates an `App` instance with the appropriate configuration.
    """

    auth: AuthService
    subscription: SubscriptionService
    user: UserService

    def __post_init__(self):
        self._services: list[Service] = [
            self.auth,
            self.subscription,
            self.user,
        ]
        for service in self._services:
            service._app = self  # type: ignore

    async def shutdown(self) -> None:
        for service in self._services:
            await service.destroy()
