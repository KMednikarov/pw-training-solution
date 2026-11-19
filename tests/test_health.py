from playwright.sync_api import APIRequestContext
import pytest

@pytest.mark.xfail(reason="BUG-123")
@pytest.mark.smoke
def test_health(api: APIRequestContext):
    response = api.get("/api/health")

    assert response.status == 201