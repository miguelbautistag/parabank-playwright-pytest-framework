from playwright.sync_api import Page
from framework.pages.base_page import BasePage


class BillPayPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.payee_name = page.locator("input[name='payee.name']")
        self.street = page.locator("input[name='payee.address.street']")
        self.city = page.locator("input[name='payee.address.city']")
        self.state = page.locator("input[name='payee.address.state']")
        self.zip_code = page.locator("input[name='payee.address.zipCode']")
        self.phone = page.locator("input[name='payee.phoneNumber']")
        self.account_number = page.locator("input[name='payee.accountNumber']")
        self.verify_account = page.locator("input[name='verifyAccount']")
        self.amount = page.locator("input[name='amount']")
        self.send_button = page.locator("input[value='Send Payment']")
        self.success_title = page.locator("#billpayResult h1.title")

    def send_payment(self, payee_data: dict) -> None:
        self.logger.info(f"Sending bill payment to {payee_data['name']}")
        self.payee_name.fill(payee_data["name"])
        self.street.fill(payee_data["address"])
        self.city.fill(payee_data["city"])
        self.state.fill(payee_data["state"])
        self.zip_code.fill(payee_data["zipCode"])
        self.phone.fill(payee_data["phone"])
        self.account_number.fill(payee_data["account"])
        self.verify_account.fill(payee_data["account"])
        self.amount.fill(payee_data["amount"])
        self.send_button.click()