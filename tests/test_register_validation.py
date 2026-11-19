import pytest
from playwright.sync_api import APIRequestContext


VALID_PAYLOAD = {
    "username": "qa_engineer",
    "email": "qa@example.com",
    "password": "StrongPass123!",
    "age": 30,
    "country": "US",
    "acceptTerms": True
}


def test_register_weak_password(api: APIRequestContext):
    payload = {
        **VALID_PAYLOAD,
        "password": "abc"
    }

    response = api.post(
        "/api/validation/register",
        data=payload
    )

    assert response.status == 422

    body = response.json()

    assert "password" in body["errors"]


@pytest.mark.parametrize(
    "field, value",
    [
        pytest.param("username", "ab", id="short-username"),
        pytest.param("email", "invalid-email", id="invalid-email"),
        pytest.param("age", 17, id="underage"),
        pytest.param("country", "XX", id="unknown-country"),
        pytest.param("acceptTerms", False, id="terms-not-accepted"),
    ]
)
def test_register_invalid_payload(
    api: APIRequestContext,
    field: str,
    value
):
    payload = {
        **VALID_PAYLOAD,
        field: value
    }

    response = api.post(
        "/api/validation/register",
        data=payload
    )

    assert response.status == 422

    body = response.json()

    assert field in body["errors"]
    assert len(body["errors"][field]) > 0

    assert response.headers["content-type"].startswith(
        "application/problem+json"
    )


def test_register_valid_payload(api: APIRequestContext):
    response = api.post(
        "/api/validation/register",
        data=VALID_PAYLOAD
    )

    assert response.status == 201, response.text()

    user = response.json()["data"]

    assert user["username"] == VALID_PAYLOAD["username"]
    assert user["email"] == VALID_PAYLOAD["email"]
    assert user["age"] == VALID_PAYLOAD["age"]
    assert user["country"] == VALID_PAYLOAD["country"]

    assert "password" not in user