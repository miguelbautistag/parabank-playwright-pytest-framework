from playwright.sync_api import Page, Locator
from framework.pages.base_page import BasePage


class RegisterPage(BasePage):
    """
    Encapsulates interactions and element definitions for the Parabank Registration Page.
    Follows Page Object Model (POM) standards.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = page.locator("input[id='customer.firstName']")
        self.last_name_input = page.locator("input[id='customer.lastName']")
        self.street_input = page.locator("input[id='customer.address.street']")
        self.city_input = page.locator("input[id='customer.address.city']")
        self.state_input = page.locator("input[id='customer.address.state']")
        self.zip_input = page.locator("input[id='customer.address.zipCode']")
        self.phone_input = page.locator("input[id='customer.phoneNumber']")
        self.ssn_input = page.locator("input[id='customer.ssn']")
        self.username_input = page.locator("input[id='customer.username']")
        self.password_input = page.locator("input[id='customer.password']")
        self.confirm_password_input = page.locator("input[id='repeatedPassword']")
        self.submit_button = page.get_by_role("button", name="Register").or_(
            page.locator("input[value='Register']")
        )
        self.success_title = page.locator("h1.title")
        self.welcome_message = page.get_by_text("Your account was created successfully. You are now logged in.")

    def register_user(self, user_data: dict) -> None:
        """
        Executes the user registration form submission workflow.
        Assertions belong in the test layer, not in the Page Object.
        """
        self.logger.info(f"Initiating registration workflow for user: {user_data.get('username')}")

        self.first_name_input.fill(user_data["firstName"])
        self.last_name_input.fill(user_data["lastName"])
        self.street_input.fill(user_data["street"])
        self.city_input.fill(user_data["city"])
        self.state_input.fill(user_data["state"])
        self.zip_input.fill(user_data["zipCode"])
        self.phone_input.fill(user_data["phoneNumber"])
        self.ssn_input.fill(user_data["ssn"])
        self.username_input.fill(user_data["username"])
        self.password_input.fill(user_data["password"])
        self.confirm_password_input.fill(user_data["password"])

        self.submit_button.click()