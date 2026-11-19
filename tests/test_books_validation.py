import pytest
from clients.books_client import BooksClient


@pytest.mark.parametrize(
    "invalid_fields",
    [
        pytest.param({"title": ""}, id="empty-title"),
        pytest.param({"author": ""}, id="empty-author"),
        pytest.param({"price": -1}, id="negative-price"),
    ]
)
def test_invalid_book(
    books: BooksClient,
    invalid_fields: dict
):
    valid = {
        "title": "Validation Test Book",
        "author": "QA Engineer",
        "price": 19.99,
        "rating": 4.5
    }

    payload = {**valid, **invalid_fields}

    response = books.create(payload)

    try:
        assert response.status == 400, response.text()

    finally:
        if response.status == 201:
            book_id = response.json()["data"]["id"]
            books.delete(book_id)


@pytest.mark.parametrize(
    "rating, expected_status",
    [
        pytest.param(-0.1, 400, id="below-minimum"),
        pytest.param(0, 201, id="minimum"),
        pytest.param(5, 201, id="maximum"),
        pytest.param(5.1, 400, id="above-maximum"),
    ]
)
def test_book_rating_boundaries(
    books: BooksClient,
    rating: float,
    expected_status: int
):
    payload = {
        "title": "Rating Boundary Test",
        "author": "QA Engineer",
        "price": 19.99,
        "rating": rating
    }

    response = books.create(payload)

    try:
        assert response.status == expected_status, response.text()

        if expected_status == 201:
            assert response.json()["data"]["rating"] == rating

    finally:
        if response.status == 201:
            book_id = response.json()["data"]["id"]

            deleted = books.delete(book_id)

            assert deleted.status == 200