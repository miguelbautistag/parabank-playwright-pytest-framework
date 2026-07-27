from playwright.sync_api import Page
from framework.pages.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = page.locator("input[name='username']")
        self.password_input = page.locator("input[name='password']")
        self.login_button = page.locator("input[value='Log In']")
        self.register_link = page.locator("a[href*='register.htm']")
        self.logout_link = page.locator("a[href*='logout.htm']")
        self.error_message = page.locator("p.error")

    def ensure_unauthenticated(self) -> None:
        """
        Ensures any lingering session on the current page is terminated
        so login operations occur from a clean state.
        """
        if self.logout_link.is_visible():
            self.logger.info("Active session detected. Executing logout.")
            self.logout_link.click()

    def navigate(self, path: str = "") -> None:
        super().navigate(path)
        self.ensure_unauthenticated()

    def login(self, username: str, password: str) -> None:
        self.logger.info(f"Attempting login for user: {username}")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def navigate_to_registration(self) -> None:
        self.register_link.click()