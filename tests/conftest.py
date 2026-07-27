import os
import allure
import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from config.settings import Config
from framework.pages.login_page import LoginPage
from framework.pages.register_page import RegisterPage
from framework.utils.data_factory import DataFactory
from framework.api.bank_client import BankApiClient


@pytest.fixture(scope="function")
def browser_context(browser: Browser) -> BrowserContext:
    """Function-scoped context ensuring isolated state per test worker."""
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        ignore_https_errors=True,
    )
    yield context
    context.clear_cookies()
    context.close()


@pytest.fixture(scope="function")
def page(browser_context: BrowserContext) -> Page:
    """Function-scoped page fixture configured with centralized timeouts."""
    page = browser_context.new_page()
    page.set_default_timeout(Config.DEFAULT_TIMEOUT)
    yield page
    page.close()


@pytest.fixture(scope="function")
def registered_user_session(page: Page) -> dict:
    """Precondition fixture delivering a freshly registered user session via UI."""
    login_page = LoginPage(page)
    register_page = RegisterPage(page)
    user_data = DataFactory.create_user_payload()

    login_page.navigate("register.htm")
    register_page.register_user(user_data)
    return user_data


@pytest.fixture(scope="session")
def api_client() -> BankApiClient:
    """Stateless or session-scoped API client for background state setup."""
    return BankApiClient()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hooks into Pytest reporting to capture screenshots on failure."""
    outcome = yield
    report = outcome.get_result()

    # Capture screenshots for failures during execution ('call') or setup phase
    if report.failed and report.when in ("call", "setup"):
        page_instance = item.funcargs.get("page", None)
        if page_instance and not page_instance.is_closed():
            try:
                screenshot = page_instance.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"failure_{item.name}_{report.when}",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                # Prevent hook failure from obscuring the root test exception
                print(f"Failed to capture allure screenshot: {e}")