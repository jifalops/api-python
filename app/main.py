import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.app import App
from app.auth.router import AuthRouter
from app.auth.router_fastapi import AuthRouterFastApi
from app.auth.service import AuthService
from config import LOGGING_LEVEL

logging.basicConfig(level=LOGGING_LEVEL)
logging.debug("Initializing App...")

app = App(auth=AuthService())

routers = [
    AuthRouterFastApi(router=AuthRouter(service=app.auth)),
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

logging.info("App initialized!")
