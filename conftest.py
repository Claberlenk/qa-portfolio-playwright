import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


# ── UI fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def logged_in(page: Page) -> Page:
    """Navigate to saucedemo and log in as standard_user."""
    lp = LoginPage(page)
    lp.navigate()
    lp.login("standard_user", "secret_sauce")
    return page
