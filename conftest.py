import jwt
import pytest
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

from app.app import App
from app.auth.repo_memory import AuthRepoMemory
from app.auth.router import AuthRouter
from app.auth.service import AuthService
from app.error import AppError
from app.subscription.adapters.router_webhooks_mock import (
    SubscriptionRouterWebhooksMock,
)
from app.subscription.adapters.service_mock import SubscriptionServiceMock
from app.subscription.router import SubscriptionRouter
from app.user.repo_memory import UserRepoMemory
from app.user.service import UserService


@pytest.fixture
def app() -> App:
    """The default app fixture for unit tests."""
    return App(
        auth=AuthService(repo=AuthRepoMemory()),
        subscription=SubscriptionServiceMock(),
        user=UserService(repo=UserRepoMemory()),
    )


@pytest.fixture
def app_router(app: App) -> FastAPI:
    routers: list[APIRouter] = [
        AuthRouter(service=app.auth),
        SubscriptionRouter(
            service=app.subscription, webhook_handler=SubscriptionRouterWebhooksMock()
        ),
    ]
    router = FastAPI()
    for r in routers:
        router.include_router(r)

    async def app_error_handler(_: Request, e: AppError):
        return JSONResponse(
            status_code=e.status,
            content={
                "error": {
                    "code": e.code,
                    "message": e.message,
                }
            },
        )

    router.exception_handler(AppError)(app_error_handler)

    return router


@pytest.fixture
def client(app_router: FastAPI) -> TestClient:
    token = jwt.encode(payload={"sub": "test_user"}, key="test_secret")
    return TestClient(
        app_router,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )


@pytest.fixture
def client2(app_router: FastAPI) -> TestClient:
    token = jwt.encode(payload={"sub": "test_user2"}, key="test_secret")
    return TestClient(
        app_router,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )


@pytest.fixture
def client_no_auth(app_router: FastAPI) -> TestClient:
    return TestClient(app_router)


@pytest.fixture
def client_admin(app_router: FastAPI) -> TestClient:
    token = jwt.encode(
        payload={
            "sub": "test_user",
            "role": "admin",
        },
        key="test_secret",
    )
    return TestClient(
        app_router,
        headers={
            "Authorization": f"Bearer {token}",
        },
    )


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if "_integration_test" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "_e2e_test" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "_test.py" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
