import base64

from playwright.sync_api import APIRequestContext

from clients.auth_client import AuthClient


def test_static_bearer_token(api: APIRequestContext) -> None:
    response = api.get(
        "/api/auth/bearer",
        headers={"Authorization": "Bearer apibee-token-123"},
    )
    assert response.status == 200


def test_api_key_header(api: APIRequestContext) -> None:
    response = api.get(
        "/api/auth/api-key/header",
        headers={"X-API-Key": "apibee-key-123"},
    )
    assert response.status == 200


def test_wrong_api_key_is_rejected(api: APIRequestContext) -> None:
    response = api.get(
        "/api/auth/api-key/header",
        headers={"X-API-Key": "wrong"},
    )
    assert response.status == 401


def test_basic_authentication(api: APIRequestContext) -> None:
    credentials = base64.b64encode(b"apibee:password123").decode()
    response = api.get(
        "/api/auth/basic",
        headers={"Authorization": f"Basic {credentials}"},
    )
    assert response.status == 200


def test_me_with_token_returns_200(admin_auth: AuthClient) -> None:
    assert admin_auth.me().status == 200


def test_me_without_token_returns_401(auth: AuthClient) -> None:
    response = auth.me()
    assert response.status == 401
    assert response.json()["error"] == "Unauthorized"


def test_admin_endpoint_allows_admin(admin_auth: AuthClient) -> None:
    assert admin_auth.admin_only().status == 200


def test_admin_endpoint_forbids_plain_user(user_auth: AuthClient) -> None:
    assert user_auth.admin_only().status == 403
