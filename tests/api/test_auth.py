import pytest

from utils.helpers import api_post


@pytest.mark.api
class TestLogin:

    def test_successful_login_returns_200(self) -> None:
        r = api_post("/login", {"email": "eve.holt@reqres.in", "password": "cityslicka"})
        assert r.status_code == 200

    def test_successful_login_returns_token(self) -> None:
        r = api_post("/login", {"email": "eve.holt@reqres.in", "password": "cityslicka"})
        assert "token" in r.json()

    def test_login_missing_password_returns_400(self) -> None:
        r = api_post("/login", {"email": "eve.holt@reqres.in"})
        assert r.status_code == 400

    def test_login_missing_password_error_message(self) -> None:
        r = api_post("/login", {"email": "eve.holt@reqres.in"})
        assert r.json().get("error") == "Missing password"

    def test_login_missing_email_returns_400(self) -> None:
        r = api_post("/login", {"password": "cityslicka"})
        assert r.status_code == 400


@pytest.mark.api
class TestRegister:

    def test_successful_register_returns_200(self) -> None:
        r = api_post("/register", {"email": "eve.holt@reqres.in", "password": "pistol"})
        assert r.status_code == 200

    def test_successful_register_returns_id_and_token(self) -> None:
        r = api_post("/register", {"email": "eve.holt@reqres.in", "password": "pistol"})
        body = r.json()
        assert "id" in body
        assert "token" in body

    def test_register_missing_password_returns_400(self) -> None:
        r = api_post("/register", {"email": "sydney@fife"})
        assert r.status_code == 400

    def test_register_missing_password_error_message(self) -> None:
        r = api_post("/register", {"email": "sydney@fife"})
        assert r.json().get("error") == "Missing password"

    def test_register_undefined_user_returns_400(self) -> None:
        r = api_post("/register", {"email": "unknown@user.com", "password": "pass"})
        assert r.status_code == 400
