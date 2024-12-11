import pytest
from pydantic import ValidationError

from app.auth.models import SignUpData


def test_signup_data_valid():
    data = SignUpData(email="test@example.com", password="strongpassword123")
    assert data.email == "test@example.com"
    assert data.password == "strongpassword123"


def test_signup_data_invalid_email():
    with pytest.raises(ValidationError):
        SignUpData(email="invalid-email", password="strongpassword123")


def test_signup_data_missing_email():
    with pytest.raises(ValidationError):
        SignUpData(password="strongpassword123")


def test_signup_data_missing_password():
    with pytest.raises(ValidationError):
        SignUpData(email="test@example.com")
