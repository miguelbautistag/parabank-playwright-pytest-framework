import pytest
from playwright.sync_api import Page, expect
from framework.pages.login_page import LoginPage
from framework.pages.register_page import RegisterPage
from framework.pages.overview_page import OverviewPage
from framework.pages.transfer_page import TransferPage
from framework.pages.billpay_page import BillPayPage
from framework.utils.data_factory import DataFactory


@pytest.mark.ui
@pytest.mark.smoke
def test_ui_e2e_user_registration(page: Page) -> None:
    """
    Validates end-to-end user registration workflow.
    Guarantees unique payload generation, dynamic form submission, and post-registration welcome state.
    """
    login_page = LoginPage(page)
    register_page = RegisterPage(page)
    user_data = DataFactory.create_user_payload()

    login_page.navigate("register.htm")
    register_page.register_user(user_data)

    expect(register_page.welcome_message).to_be_visible()
    expect(register_page.success_title).to_contain_text(f"Welcome {user_data['username']}")


@pytest.mark.ui
@pytest.mark.regression
def test_ui_e2e_user_login_and_session_persistence(
    page: Page, registered_user_session: dict
) -> None:
    """
    Validates session persistence, explicit logout, and subsequent re-authentication.
    Uses registered_user_session fixture for context-isolated preconditions in parallel mode.
    """
    login_page = LoginPage(page)
    overview_page = OverviewPage(page)

    # Verify active session from fixture registration before logout
    expect(overview_page.logout_link).to_be_visible()
    overview_page.logout_link.click()

    # Explicit re-authentication using isolated user credentials
    login_page.login(
        username=registered_user_session["username"],
        password=registered_user_session["password"],
    )

    expect(overview_page.welcome_message).to_be_visible()
    expect(overview_page.welcome_message).to_contain_text(
        f"Welcome {registered_user_session['firstName']}"
    )


@pytest.mark.ui
@pytest.mark.regression
def test_ui_e2e_fund_transfer_execution(
    page: Page, registered_user_session: dict
) -> None:
    """
    Validates end-to-end fund transfer between accounts for an authenticated session.
    Relies on Playwright auto-waiting for link actionability and DOM rendering.
    """
    overview_page = OverviewPage(page)
    transfer_page = TransferPage(page)

    # Web-first assertion ensures session readiness before navigation
    expect(overview_page.transfer_funds_link).to_be_visible()
    overview_page.transfer_funds_link.click()

    transfer_page.transfer_funds(amount="150")

    expect(transfer_page.success_title).to_contain_text("Transfer Complete!")


@pytest.mark.ui
@pytest.mark.regression
def test_ui_e2e_bill_payment_execution(
    page: Page, registered_user_session: dict
) -> None:
    """
    Validates end-to-end bill payment workflow execution.
    Combines dynamic payee data generation with UI submission and web-first verification.
    """
    overview_page = OverviewPage(page)
    billpay_page = BillPayPage(page)
    payee_data = DataFactory.create_bill_pay_payload()

    # Web-first assertion ensures link is actionable on active worker context
    expect(overview_page.bill_pay_link).to_be_visible()
    overview_page.bill_pay_link.click()

    billpay_page.send_payment(payee_data)

    expect(billpay_page.success_title).to_contain_text("Bill Payment Complete")