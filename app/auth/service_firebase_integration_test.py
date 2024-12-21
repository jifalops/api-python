import pytest

from app.app import App
from app.auth.service_firebase import AuthServiceFirebase


@pytest.fixture
def app(app: App) -> App:
    app.auth = AuthServiceFirebase()
    app.__post_init__()
    return app
