import time
from typing import Callable


def wait_until(check: Callable[[], bool], timeout: float = 30.0, interval: float = 1.0) -> None:
    deadline = time.monotonic() + timeout
    while not check():
        if time.monotonic() >= deadline:
            raise AssertionError(f"Condition not met within {timeout} seconds")
        time.sleep(interval)


def wait_for_job(
    api,
    status_url: str,
    expected_status: str,
    timeout: float = 30.0,
    interval: float = 0.5,
) -> dict:
    result: dict | None = None

    def job_reached_expected_status() -> bool:
        nonlocal result
        response = api.get(status_url)
        if response.status != 200:
            return False
        result = response.json()
        return result["status"] == expected_status

    wait_until(job_reached_expected_status, timeout=timeout, interval=interval)
    assert result is not None
    return result