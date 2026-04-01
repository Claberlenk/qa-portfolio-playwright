from playwright.sync_api import Page


class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart_items = page.locator(".cart_item")
        self.checkout_button = page.locator("[data-test='checkout']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")

    def navigate(self) -> None:
        self.page.goto(self.URL)

    def get_item_names(self) -> list[str]:
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def get_item_count(self) -> int:
        return self.cart_items.count()

    def remove_item(self, item_name: str) -> None:
        item = self.page.locator(
            f".cart_item:has(.inventory_item_name:text('{item_name}'))"
        )
        item.locator("button[id^='remove']").click()

    def proceed_to_checkout(self) -> None:
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()
