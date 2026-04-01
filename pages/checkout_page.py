from playwright.sync_api import Page


class CheckoutPage:
    STEP_ONE_URL = "https://www.saucedemo.com/checkout-step-one.html"
    STEP_TWO_URL = "https://www.saucedemo.com/checkout-step-two.html"
    COMPLETE_URL = "https://www.saucedemo.com/checkout-complete.html"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.cancel_button = page.locator("[data-test='cancel']")
        self.summary_total = page.locator(".summary_total_label")
        self.complete_header = page.locator(".complete-header")
        self.error_message = page.locator("[data-test='error']")

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(postal_code)

    def continue_to_step_two(self) -> None:
        self.continue_button.click()

    def finish_order(self) -> None:
        self.finish_button.click()

    def get_total(self) -> str:
        return self.summary_total.inner_text()

    def get_complete_header(self) -> str:
        return self.complete_header.inner_text()

    def get_error_message(self) -> str:
        return self.error_message.inner_text()
