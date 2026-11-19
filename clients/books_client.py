from typing import Any

from playwright.sync_api import APIRequestContext, APIResponse


class BooksClient:
    ROUTE = "/api/Books"

    def __init__(self, api: APIRequestContext) -> None:
        self.api = api

    def list(self, params: dict[str, Any] | None = None) -> APIResponse:
        return self.api.get(self.ROUTE, params=params)

    def get(self, book_id: int) -> APIResponse:
        return self.api.get(f"{self.ROUTE}/{book_id}")

    def create(self, body: dict[str, Any]) -> APIResponse:
        return self.api.post(self.ROUTE, data=body)

    def replace(self, book_id: int, body: dict[str, Any]) -> APIResponse:
        return self.api.put(f"{self.ROUTE}/{book_id}", data=body)

    def update(self, book_id: int, body: dict[str, Any]) -> APIResponse:
        return self.api.patch(f"{self.ROUTE}/{book_id}", data=body)

    def patch(self, book_id: int, body: dict[str, Any]) -> APIResponse:
        return self.update(book_id, body)

    def delete(self, book_id: int) -> APIResponse:
        return self.api.delete(f"{self.ROUTE}/{book_id}")

    def genres(self) -> APIResponse:
        return self.api.get(f"{self.ROUTE}/genres")

    def count(self) -> APIResponse:
        return self.api.get(f"{self.ROUTE}/count")
