from playwright.sync_api import APIRequestContext, APIResponse


class AuthClient:
    def __init__(self, api: APIRequestContext) -> None:
        self.api = api

    def login(self, username: str, password: str) -> APIResponse:
        return self.api.post(
            "/api/auth/jwt/login",
            data={"username": username, "password": password},
        )

    def me(self) -> APIResponse:
        return self.api.get("/api/auth/jwt/me")

    def admin_only(self) -> APIResponse:
        return self.api.get("/api/auth/jwt/admin")
