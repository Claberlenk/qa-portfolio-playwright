import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.mark.ui
class TestCart:

    @pytest.fixture(autouse=True)
    def add_items(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.add_item_to_cart("Sauce Labs Backpack")
        inv.add_item_to_cart("Sauce Labs Bike Light")
        inv.go_to_cart()
        self.page = logged_in

    def test_cart_shows_added_items(self) -> None:
        cart = CartPage(self.page)
        names = cart.get_item_names()
        assert "Sauce Labs Backpack" in names
        assert "Sauce Labs Bike Light" in names

    def test_cart_item_count(self) -> None:
        cart = CartPage(self.page)
        assert cart.get_item_count() == 2

    def test_remove_item_from_cart(self) -> None:
        cart = CartPage(self.page)
        cart.remove_item("Sauce Labs Backpack")
        assert "Sauce Labs Backpack" not in cart.get_item_names()
        assert cart.get_item_count() == 1

    def test_continue_shopping_returns_to_inventory(self) -> None:
        cart = CartPage(self.page)
        cart.continue_shopping()
        expect(self.page).to_have_url("https://www.saucedemo.com/inventory.html")

    def test_checkout_button_navigates(self) -> None:
        cart = CartPage(self.page)
        cart.proceed_to_checkout()
        expect(self.page).to_have_url(
            "https://www.saucedemo.com/checkout-step-one.html"
        )
