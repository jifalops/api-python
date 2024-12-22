import logging
from http import HTTPStatus

from fastapi.testclient import TestClient


def test_sign_up(client: TestClient, client_no_auth: TestClient):
    response = client.post("/auth/sign-up")
    assert response.status_code == HTTPStatus.OK

    response = client_no_auth.post("/auth/sign-up")
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_set_role(
    client: TestClient,
    client2: TestClient,
    client_no_auth: TestClient,
    client_admin: TestClient,
):
    # No users
    response = client.post(
        "/auth/set-role", params={"user_id": "test_user", "role": "admin"}
    )
    logging.debug(response.json())
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    # One user
    client.post("/auth/sign-up")
    response = client.post(
        "/auth/set-role", params={"user_id": "test_user", "role": "admin"}
    )
    assert response.status_code == HTTPStatus.OK

    # No token
    response = client_no_auth.post(
        "/auth/set-role", params={"user_id": "test_user", "role": "admin"}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN

    # Two users
    client2.post("/auth/sign-up")
    response = client2.post(
        "/auth/set-role", params={"user_id": "test_user2", "role": "admin"}
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    # Add admin
    response = client_admin.post(
        "/auth/set-role", params={"user_id": "test_user2", "role": "admin"}
    )
    assert response.status_code == HTTPStatus.OK

    # Remove admin
    response = client_admin.post("/auth/set-role", params={"user_id": "test_user2"})
    assert response.status_code == HTTPStatus.OK
