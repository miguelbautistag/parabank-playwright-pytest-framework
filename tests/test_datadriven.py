import pytest
from playwright.sync_api import Page, expect
from framework.pages.login_page import LoginPage


@pytest.mark.datadriven
@pytest.mark.ui
@pytest.mark.parametrize(
    "username,password",
    [
        ("invalid_alpha", "pass123"),
        ("user_beta", "wrong_pass"),
        ("admin_test", "123456"),
    ],
)
def test_datadriven_login_validation(page: Page, username: str, password: str):
    """
    Validates parameterized login failure behavior across multiple invalid credential sets.
    """
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)

    expect(login_page.error_message).to_be_visible()