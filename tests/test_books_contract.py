from pydantic import TypeAdapter
from clients.books_client import BooksClient

from schemas.book import Book


def test_books_list_contract(books: BooksClient):
    response = books.list({"limit": 5})

    assert response.status == 200

    books = response.json()

    assert len(books) > 0

    TypeAdapter(list[Book]).validate_python(books)


def test_single_book_contract(
    books: BooksClient,
    book: dict
):
    response = books.get(book["id"])

    assert response.status == 200

    validated_book = Book.model_validate(response.json())

    assert validated_book.id == book["id"]