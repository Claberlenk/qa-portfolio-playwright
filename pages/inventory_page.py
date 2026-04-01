from playwright.sync_api import Page


class InventoryPage:
    URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.inventory_list = page.locator(".inventory_list")
        self.inventory_items = page.locator(".inventory_item")
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_dropdown = page.locator("[data-test='product-sort-container']")
        self.burger_menu = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")

    def navigate(self) -> None:
        self.page.goto(self.URL)

    def add_item_to_cart(self, item_name: str) -> None:
        """Add item by its visible name."""
        item = self.page.locator(
            f".inventory_item:has(.inventory_item_name:text('{item_name}'))"
        )
        item.locator("button").click()

    def remove_item_from_cart(self, item_name: str) -> None:
        item = self.page.locator(
            f".inventory_item:has(.inventory_item_name:text('{item_name}'))"
        )
        item.locator("button").click()

    def get_cart_count(self) -> int:
        if not self.cart_badge.is_visible():
            return 0
        return int(self.cart_badge.inner_text())

    def get_item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def get_item_prices(self) -> list[float]:
        raw = self.page.locator(".inventory_item_price").all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def sort_by(self, option: str) -> None:
        """option: 'az', 'za', 'lohi', 'hilo'"""
        self.sort_dropdown.select_option(option)

    def go_to_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.burger_menu.click()
        self.logout_link.click()
