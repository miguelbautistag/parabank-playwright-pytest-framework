from playwright.sync_api import Page
from framework.pages.base_page import BasePage


class TransferPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.amount_input = page.locator("#amount")
        self.from_account_select = page.locator("#fromAccountId")
        self.to_account_select = page.locator("#toAccountId")
        self.transfer_button = page.locator("input[value='Transfer']")
        self.success_title = page.locator("#showResult h1.title")

    def transfer_funds(self, amount: str) -> None:
        self.logger.info(f"Transferring {amount} between accounts")
        self.amount_input.fill(amount)
        # Rely on Playwright's native auto-waiting for element actionability
        self.transfer_button.click()