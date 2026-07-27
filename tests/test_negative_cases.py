import pytest
from playwright.sync_api import Page, expect
from framework.pages.login_page import LoginPage
from framework.pages.overview_page import OverviewPage
from framework.pages.billpay_page import BillPayPage


@pytest.mark.ui
@pytest.mark.regression
def test_negative_invalid_login_credentials(page: Page):
    """Validates error message display when submitting unauthenticated invalid credentials."""
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("invalid_user_x", "WrongPassword123")

    expect(login_page.error_message).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_negative_bill_pay_empty_submission(page: Page, registered_user_session: dict):
    """Validates form validation error when submitting an empty bill payment form."""
    overview_page = OverviewPage(page)
    billpay_page = BillPayPage(page)

    overview_page.bill_pay_link.click()
    billpay_page.send_button.click()

    payee_error = page.locator("span[id='validationModel-name']")
    expect(payee_error).to_be_visible()


@pytest.mark.api
def test_negative_api_invalid_customer_lookup(api_client):
    """Validates API error response codes for non-existent customer records."""
    response = api_client.get_customer_details(9999999)
    assert response.status_code in [400, 404, 500]