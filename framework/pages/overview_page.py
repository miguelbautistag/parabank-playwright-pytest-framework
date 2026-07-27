from playwright.sync_api import Page
from framework.pages.base_page import BasePage


class OverviewPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.accounts_table = page.locator("#accountTable")
        self.welcome_message = page.locator("p.smallText")
        self.open_new_account_link = page.get_by_role("link", name="Open New Account")
        self.transfer_funds_link = page.get_by_role("link", name="Transfer Funds")
        self.bill_pay_link = page.get_by_role("link", name="Bill Pay")
        self.logout_link = page.get_by_role("link", name="Log Out")

    def get_first_account_id(self) -> str:
        first_account = self.accounts_table.locator("tbody tr a").first
        first_account.wait_for(state="visible")
        return first_account.inner_text()