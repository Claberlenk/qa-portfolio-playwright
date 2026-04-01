import pytest
import requests

from utils.helpers import api_get, api_post, api_put, api_patch, api_delete


@pytest.mark.api
class TestGetUsers:

    def test_get_users_list_returns_200(self) -> None:
        r = api_get("/users", params={"page": 1})
        assert r.status_code == 200

    def test_get_users_list_schema(self) -> None:
        r = api_get("/users", params={"page": 1})
        body = r.json()
        assert "data" in body
        assert "total" in body
        assert "page" in body
        assert isinstance(body["data"], list)

    def test_get_users_page_2(self) -> None:
        r = api_get("/users", params={"page": 2})
        assert r.status_code == 200
        assert r.json()["page"] == 2

    def test_get_single_user_returns_200(self) -> None:
        r = api_get("/users/2")
        assert r.status_code == 200

    def test_get_single_user_schema(self) -> None:
        r = api_get("/users/2")
        user = r.json()["data"]
        assert "id" in user
        assert "email" in user
        assert "first_name" in user
        assert "last_name" in user

    def test_get_single_user_correct_id(self) -> None:
        r = api_get("/users/2")
        assert r.json()["data"]["id"] == 2

    def test_get_nonexistent_user_returns_404(self) -> None:
        r = api_get("/users/9999")
        assert r.status_code == 404

    def test_get_nonexistent_user_empty_body(self) -> None:
        r = api_get("/users/9999")
        assert r.json() == {}


@pytest.mark.api
class TestCreateUser:

    def test_create_user_returns_201(self) -> None:
        r = api_post("/users", {"name": "morpheus", "job": "leader"})
        assert r.status_code == 201

    def test_create_user_response_contains_id(self) -> None:
        r = api_post("/users", {"name": "morpheus", "job": "leader"})
        body = r.json()
        assert "id" in body
        assert "createdAt" in body

    def test_create_user_name_is_returned(self) -> None:
        r = api_post("/users", {"name": "neo", "job": "chosen one"})
        assert r.json()["name"] == "neo"


@pytest.mark.api
class TestUpdateUser:

    def test_put_user_returns_200(self) -> None:
        r = api_put("/users/2", {"name": "morpheus", "job": "zion resident"})
        assert r.status_code == 200

    def test_put_user_updated_at_present(self) -> None:
        r = api_put("/users/2", {"name": "morpheus", "job": "zion resident"})
        assert "updatedAt" in r.json()

    def test_patch_user_returns_200(self) -> None:
        r = api_patch("/users/2", {"job": "zion resident"})
        assert r.status_code == 200

    def test_patch_user_updated_at_present(self) -> None:
        r = api_patch("/users/2", {"job": "zion resident"})
        assert "updatedAt" in r.json()


@pytest.mark.api
class TestDeleteUser:

    def test_delete_user_returns_204(self) -> None:
        r = api_delete("/users/2")
        assert r.status_code == 204

    def test_delete_user_empty_response_body(self) -> None:
        r = api_delete("/users/2")
        assert r.text == ""
