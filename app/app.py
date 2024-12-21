from dataclasses import dataclass

from app.auth.service import AuthService
from app.service import Service
from app.subscription.service import SubscriptionService
from app.subscription_portal.service import SubscriptionPortalService
from app.user.service import UserService


@dataclass
class App:
    """
    The container for services that the application uses.

    Each entry point (main.py, testing, etc.) creates an `App` instance with the appropriate configuration.
    """

    auth: AuthService
    subscription: SubscriptionService
    subscription_portal: SubscriptionPortalService
    user: UserService

    def __post_init__(self):
        self._services: list[Service] = [
            self.auth,
            self.subscription,
            self.subscription_portal,
            self.user,
        ]
        for service in self._services:
            service._app = self  # type: ignore

    async def shutdown(self) -> None:
        for service in self._services:
            await service.destroy()
