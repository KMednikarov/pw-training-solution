from playwright.sync_api import APIRequestContext, Page, expect

from helpers.waiting import wait_until


def test_book_created_by_api_appears_in_ui(page: Page, book: dict) -> None:
    # arrange: the `book` fixture created the record through the API
    page.goto("/books")

    # act and assert in the browser
    page.get_by_placeholder("Search").fill(book["title"])
    expect(page.get_by_role("row", name=book["title"])).to_be_visible()


def test_deleting_in_ui_removes_record_from_api(
    page: Page, api: APIRequestContext, book: dict
) -> None:
    page.goto(f"/books/{book['id']}")
    page.get_by_role("button", name="Delete").click()
    page.get_by_role("button", name="Confirm").click()

    # assert the backend state, not just the toast message
    wait_until(lambda: api.get(f"/api/Books/{book['id']}").status == 404, timeout=10)