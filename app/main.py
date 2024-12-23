import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.app import App
from app.auth.repo_firebase import AuthRepoFirebase
from app.auth.router import AuthRouter
from app.auth.service import AuthService
from app.error import AppError
from app.subscription.adapters.repo_memory import SubscriptionRepoMemory
from app.subscription.adapters.router_webhooks_stripe import (
    SubscriptionRouterWebhooksStripe,
)
from app.subscription.adapters.service_stripe import SubscriptionServiceStripe
from app.subscription.router import SubscriptionRouter
from app.user.repo_memory import UserRepoMemory
from app.user.service import UserService
from config import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)
logging.debug("Initializing App...")

app = App(
    auth=AuthService(repo=AuthRepoFirebase()),
    subscription=SubscriptionServiceStripe(repo=SubscriptionRepoMemory()),
    user=UserService(repo=UserRepoMemory()),
)

routers: list[APIRouter] = [
    AuthRouter(service=app.auth),
    SubscriptionRouter(
        service=app.subscription,
        webhook_handler=SubscriptionRouterWebhooksStripe(service=app.subscription),
    ),
]


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield
    await app.shutdown()


app_router = FastAPI(lifespan=lifespan)


app_router.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app_router.include_router(router)
app_router.get("/")(lambda: {"Hello": "World"})


@app_router.exception_handler(AppError)
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


logging.info("App initialized!")
