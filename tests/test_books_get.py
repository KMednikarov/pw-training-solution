import pytest

from clients.books_client import BooksClient


@pytest.mark.smoke
def test_list_books(books: BooksClient) -> None:
    response = books.list({"limit": 5, "sort": "title"})

    assert response.status == 200
    assert "application/json" in response.headers["content-type"]
    assert int(response.headers["x-total-count"]) >= 1

    books = response.json()
    assert isinstance(books, list)
    assert 1 <= len(books) <= 5

    first = books[0]
    assert isinstance(first["id"], int)
    assert first["title"] != ""


def test_get_missing_book_returns_404(books: BooksClient) -> None:
    response = books.get(999999)

    assert response.status == 404
    assert response.json()["error"] == "Not Found"


@pytest.mark.smoke
def test_get_books_status(books: BooksClient):
    response = books.list()

    assert response.status == 200


@pytest.mark.smoke
def test_get_books_response_body(books: BooksClient):
    response = books.list()

    assert response.status == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_filter_books_by_genre(books: BooksClient):
    response = books.list({"genre": "fantasy"})

    assert response.status == 200

    books = response.json()

    assert len(books) > 0

    for book in books:
        assert book["genre"].lower() == "fantasy"


def test_sort_books_by_price_desc(books: BooksClient):
    response = books.list({
            "limit": 5,
            "sort": "price",
            "order": "desc"
        })

    assert response.status == 200

    books = response.json()

    assert len(books) == 5

    prices = [book["price"] for book in books]

    assert prices == sorted(prices, reverse=True)


def test_books_pagination(books: BooksClient):
    response = books.list({
            "limit": 3,
            "page": 2
        })

    assert response.status == 200
    assert len(response.json()) <= 3
    assert response.headers["x-page"] == "2"


def test_get_book_genres(books: BooksClient):
    response = books.genres()

    assert response.status == 200

    genres = response.json()

    assert isinstance(genres, list)
    assert len(genres) > 0

    for genre in genres:
        assert isinstance(genre, str)


def test_books_service_unavailable(books: BooksClient):
    response = books.list({"error": 503})

    assert response.status == 503

def test_filter_books_by_author(
    books: BooksClient,
    three_books: list[dict]
):
    author = three_books[0]["author"]

    response = books.list({"author": author})

    assert response.status == 200

    books = response.json()

    assert len(books) == 3

    expected_ids = {book["id"] for book in three_books}
    actual_ids = {book["id"] for book in books}

    assert actual_ids == expected_ids

    for book in books:
        assert book["author"] == author