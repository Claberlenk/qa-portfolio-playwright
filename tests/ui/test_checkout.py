import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.mark.ui
class TestCheckout:

    @pytest.fixture(autouse=True)
    def reach_checkout(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.add_item_to_cart("Sauce Labs Backpack")
        inv.go_to_cart()
        CartPage(logged_in).proceed_to_checkout()
        self.page = logged_in

    def test_complete_checkout_flow(self) -> None:
        co = CheckoutPage(self.page)
        co.fill_info("John", "Doe", "12345")
        co.continue_to_step_two()
        expect(self.page).to_have_url(
            "https://www.saucedemo.com/checkout-step-two.html"
        )
        co.finish_order()
        expect(self.page).to_have_url(
            "https://www.saucedemo.com/checkout-complete.html"
        )
        assert "thank you" in co.get_complete_header().lower()

    def test_missing_first_name_shows_error(self) -> None:
        co = CheckoutPage(self.page)
        co.fill_info("", "Doe", "12345")
        co.continue_to_step_two()
        assert "first name is required" in co.get_error_message().lower()

    def test_missing_last_name_shows_error(self) -> None:
        co = CheckoutPage(self.page)
        co.fill_info("John", "", "12345")
        co.continue_to_step_two()
        assert "last name is required" in co.get_error_message().lower()

    def test_missing_postal_code_shows_error(self) -> None:
        co = CheckoutPage(self.page)
        co.fill_info("John", "Doe", "")
        co.continue_to_step_two()
        assert "postal code is required" in co.get_error_message().lower()

    def test_summary_displays_total(self) -> None:
        co = CheckoutPage(self.page)
        co.fill_info("John", "Doe", "12345")
        co.continue_to_step_two()
        total = co.get_total()
        assert "Total:" in total
