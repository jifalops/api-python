from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.app import App


class BaseService:
    """Base class for all services."""

    app: "App"
    """
    The app this service is part of.

    Services may call other services by using `self.app.<service>`.
    """

    def _set_app(self, app: "App") -> None:
        """Intended to be called by the `App` class only."""
        self.app = app

    async def destroy(self) -> None:
        """Clean up resources, the app is exiting."""
        pass
