from mangum import Mangum

from app.main import app_router

lambda_handler = Mangum(app_router)
