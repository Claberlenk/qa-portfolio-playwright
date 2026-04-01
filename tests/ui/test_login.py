import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utils.helpers import STANDARD_USER, LOCKED_USER


@pytest.mark.ui
class TestLogin:

    def test_successful_login(self, page: Page) -> None:
        lp = LoginPage(page)
        lp.navigate()
        lp.login(STANDARD_USER["username"], STANDARD_USER["password"])
        expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    def test_locked_user_sees_error(self, page: Page) -> None:
        lp = LoginPage(page)
        lp.navigate()
        lp.login(LOCKED_USER["username"], LOCKED_USER["password"])
        assert lp.is_error_visible()
        assert "locked out" in lp.get_error_message().lower()

    def test_invalid_password_shows_error(self, page: Page) -> None:
        lp = LoginPage(page)
        lp.navigate()
        lp.login("standard_user", "wrong_password")
        assert lp.is_error_visible()
        assert "username and password do not match" in lp.get_error_message().lower()

    def test_empty_username_shows_error(self, page: Page) -> None:
        lp = LoginPage(page)
        lp.navigate()
        lp.login("", "secret_sauce")
        assert lp.is_error_visible()
        assert "username is required" in lp.get_error_message().lower()

    def test_empty_password_shows_error(self, page: Page) -> None:
        lp = LoginPage(page)
        lp.navigate()
        lp.login("standard_user", "")
        assert lp.is_error_visible()
        assert "password is required" in lp.get_error_message().lower()

    def test_logout(self, logged_in: Page) -> None:
        from pages.inventory_page import InventoryPage
        inv = InventoryPage(logged_in)
        inv.logout()
        expect(logged_in).to_have_url("https://www.saucedemo.com/")
