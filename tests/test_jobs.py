from playwright.sync_api import APIRequestContext

from helpers.waiting import wait_for_job


def test_job_completes_successfully(api: APIRequestContext):
    response = api.post(
        "/api/jobs",
        data={
            "type": "report",
            "durationSeconds": 5
        }
    )

    assert response.status == 202

    created = response.json()["data"]
    status_url = response.headers["location"]

    assert created["status"] == "queued"
    assert status_url == created["statusUrl"]

    job = wait_for_job(
        api,
        status_url,
        expected_status="completed",
        timeout=30
    )

    assert job["id"] == created["id"]
    assert job["status"] == "completed"
    assert job["progress"] == 100
    assert job["error"] is None
    assert job["resultUrl"] is not None

    response = api.get(job["resultUrl"])

    assert response.status == 200

    result = response.json()

    assert result["jobId"] == created["id"]
    assert result["type"] == "report"
    assert result["result"] is not None


def test_job_fails(api: APIRequestContext):
    response = api.post(
        "/api/jobs",
        data={
            "type": "fail",
            "durationSeconds": 5
        }
    )

    assert response.status == 202

    created = response.json()["data"]

    job = wait_for_job(
        api,
        created["statusUrl"],
        expected_status="failed",
        timeout=30
    )

    assert job["id"] == created["id"]
    assert job["status"] == "failed"
    assert job["error"] is not None

    result_url = (
        job["resultUrl"]
        or f"/api/jobs/{job['id']}/result"
    )

    response = api.get(result_url)

    assert response.status == 409