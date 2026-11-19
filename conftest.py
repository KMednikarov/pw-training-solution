import os
from typing import Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Playwright

from clients.auth_client import AuthClient
from clients.books_client import BooksClient

test_env = os.getenv("TEST_ENV", "practice")
load_dotenv(f".env.{test_env}")

BASE_URL = os.getenv("API_BASE_URL", "https://api.testingapis.com")


def pytest_report_header(config):
    # shown at the top of every pytest run
    return f"API under test: {BASE_URL}"


@pytest.fixture(scope="session")
def api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={"Accept": "application/json"},
    )
    print(f"\n[api] request context created for {BASE_URL}")
    yield context
    context.dispose()
    print("\n[api] request context closed")

def login(playwright: Playwright, username: str, password: str) -> str:
    context = playwright.request.new_context(base_url=BASE_URL)
    response = AuthClient(context).login(username, password)
    if not 200 <= response.status < 300:
        raise AssertionError(f"Login failed with status {response.status}")
    access_token = response.json()["accessToken"]
    context.dispose()
    return access_token


@pytest.fixture
def books(api: APIRequestContext) -> BooksClient:
    return BooksClient(api)


@pytest.fixture
def auth(api: APIRequestContext) -> AuthClient:
    return AuthClient(api)


@pytest.fixture
def admin_auth(admin_api: APIRequestContext) -> AuthClient:
    return AuthClient(admin_api)


@pytest.fixture
def user_auth(user_api: APIRequestContext) -> AuthClient:
    return AuthClient(user_api)


def context_with_token(playwright: Playwright, token: str) -> APIRequestContext:
    return playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {token}",
        },
    )


@pytest.fixture(scope="session")
def admin_api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    token = login(playwright, os.environ["API_USER"], os.environ["API_PASSWORD"])
    context = context_with_token(playwright, token)
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def user_api(playwright: Playwright) -> Generator[APIRequestContext, None, None]:
    token = login(playwright, "user", "user123")
    context = context_with_token(playwright, token)
    yield context
    context.dispose()

import uuid


@pytest.fixture
def book(books: BooksClient) -> Generator[dict, None, None]:
    response = books.create(
        {
            "title": f"QA Training {uuid.uuid4().hex[:8]}",
            "author": "Test Author",
            "pages": 100,
            "price": 10.0,
        }
    )
    assert response.status == 201
    created = response.json()["data"]
    print(f"Created book ID: {created['id']}")

    yield created

    books.delete(created["id"])

@pytest.fixture
def three_books(
    books: BooksClient
) -> Generator[list[dict], None, None]:

    author = f"Test Author {uuid.uuid4().hex}"
    created_books = []

    try:
        for i in range(3):
            payload = {
                "title": f"Test Book {i + 1}",
                "author": author,
                "genre": "fantasy",
                "price": (i + 1) * 10.0
            }

            response = books.create(payload)

            assert response.status == 201

            created_books.append(response.json()["data"])

        yield created_books

    finally:
        failed_deletions = []

        for book in created_books:
            response = books.delete(book["id"])

            if response.status != 200:
                failed_deletions.append(book["id"])

        assert not failed_deletions, (
            f"Failed to delete books: {failed_deletions}"
        )