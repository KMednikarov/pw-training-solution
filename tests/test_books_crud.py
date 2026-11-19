import uuid

from playwright.sync_api import expect

from clients.books_client import BooksClient


def test_put_replaces_book(books: BooksClient, book: dict) -> None:
    payload = {
        "title": "Advanced API Testing",
        "author": "New Author",
        "isbn": "9781617299537",
        "genre": "technology",
        "publishedYear": 2025,
        "pages": 350,
        "language": "English",
        "price": 49.99,
        "rating": 4.5,
        "available": True,
        "tags": ["automation", "testing"],
    }

    response = books.replace(book["id"], payload)
    assert response.status == 200

    updated = books.get(book["id"])
    assert updated.status == 200
    for key, value in payload.items():
        assert updated.json()[key] == value


def test_patch_ignores_unknown_fields(books: BooksClient, book: dict) -> None:
    response = books.update(book["id"], {"price": 29.99, "colour": "red"})
    assert response.status == 200

    body = response.json()
    assert "colour" in body["ignored"]
    assert "price" in body["changed"]

    updated = books.get(book["id"])
    assert updated.status == 200
    assert updated.json()["price"] == 29.99
    assert "colour" not in updated.json()
    assert updated.json()["title"] == book["title"]


def test_rename_book(books: BooksClient, book: dict) -> None:
    response = books.update(book["id"], {"title": "Renamed"})
    expect(response).to_be_ok()
    assert response.json()["data"]["title"] == "Renamed"


def test_book_lifecycle(books: BooksClient) -> None:
    title = f"QA Training {uuid.uuid4().hex[:8]}"
    created = books.create(
        {"title": title, "author": "Test Author", "pages": 120, "price": 19.99}
    )
    assert created.status == 201

    book = created.json()["data"]
    book_id = book["id"]
    fetched = books.get(book_id)
    expect(fetched).to_be_ok()
    assert fetched.json()["title"] == title

    patched = books.update(book_id, {"price": 24.99})
    expect(patched).to_be_ok()
    assert patched.json()["data"]["price"] == 24.99

    deleted = books.delete(book_id)
    print('f')
    assert deleted.status == 200
    assert books.get(book_id).status == 404


def test_delete_book_twice(books: BooksClient) -> None:
    created = books.create(
        {"title": "Delete Testing", "author": "QA Engineer", "price": 15.99}
    )
    assert created.status == 201
    book_id = created.json()["data"]["id"]

    assert books.delete(book_id).status == 200
    assert books.delete(book_id).status == 404
