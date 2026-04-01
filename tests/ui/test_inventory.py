import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage


@pytest.mark.ui
class TestInventory:

    def test_inventory_page_has_items(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        assert inv.inventory_items.count() == 6

    def test_add_single_item_updates_cart_badge(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.add_item_to_cart("Sauce Labs Backpack")
        assert inv.get_cart_count() == 1

    def test_add_multiple_items(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.add_item_to_cart("Sauce Labs Backpack")
        inv.add_item_to_cart("Sauce Labs Bike Light")
        assert inv.get_cart_count() == 2

    def test_remove_item_decrements_cart(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.add_item_to_cart("Sauce Labs Backpack")
        inv.remove_item_from_cart("Sauce Labs Backpack")
        assert inv.get_cart_count() == 0

    def test_sort_by_name_az(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.sort_by("az")
        names = inv.get_item_names()
        assert names == sorted(names)

    def test_sort_by_name_za(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.sort_by("za")
        names = inv.get_item_names()
        assert names == sorted(names, reverse=True)

    def test_sort_by_price_low_to_high(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.sort_by("lohi")
        prices = inv.get_item_prices()
        assert prices == sorted(prices)

    def test_sort_by_price_high_to_low(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.sort_by("hilo")
        prices = inv.get_item_prices()
        assert prices == sorted(prices, reverse=True)

    def test_navigate_to_cart(self, logged_in: Page) -> None:
        inv = InventoryPage(logged_in)
        inv.go_to_cart()
        expect(logged_in).to_have_url("https://www.saucedemo.com/cart.html")
