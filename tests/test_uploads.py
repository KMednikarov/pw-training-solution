from playwright.sync_api import APIRequestContext


def test_upload_file(api: APIRequestContext):
    filename = "test.txt"
    description = "API automation test file"

    response = api.post(
        "/api/formdata/upload",
        multipart={
            "description": description,
            "file": {
                "name": filename,
                "mimeType": "text/plain",
                "buffer": b"Hello from Playwright!"
            }
        }
    )

    assert response.status == 201

    body = response.json()
    file_id = body["id"]

    try:
        assert body["fileName"] == filename
        assert body["description"] == description

    finally:
        response = api.delete(
            f"/api/formdata/delete/{file_id}"
        )
        assert response.ok


def test_upload_without_file(api: APIRequestContext):
    response = api.post(
        "/api/formdata/upload",
        multipart={
            "description": "Missing file"
        }
    )

    assert response.status == 400