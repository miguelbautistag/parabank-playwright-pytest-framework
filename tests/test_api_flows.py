import pytest
from framework.api.bank_client import BankApiClient


@pytest.mark.api
@pytest.mark.smoke
def test_api_chained_lifecycle(api_client: BankApiClient):
    """
    Validates REST API chained scenario lifecycle:
    Get Customer Details -> Retrieve Accounts -> Create Account -> Transfer Funds.
    """
    customer_id = 12212
    customer_res = api_client.get_customer_details(customer_id)
    assert customer_res.status_code == 200, "Customer query failed"

    accounts_res = api_client.get_accounts(customer_id)
    assert accounts_res.status_code == 200, "Account retrieval failed"

    # Execute account creation
    new_acc_res = api_client.create_account(
        customer_id=customer_id, new_account_type=0, from_account_id=12345
    )
    assert new_acc_res.status_code == 200, "Account creation failed"

    # Execute fund transfer
    transfer_res = api_client.transfer_funds(
        from_account_id=12345, to_account_id=54321, amount=100.0
    )
    assert transfer_res.status_code == 200, "Fund transfer execution failed"


@pytest.mark.api
def test_api_get_customer_profile(api_client: BankApiClient):
    response = api_client.get_customer_details(12212)
    assert response.status_code == 200


@pytest.mark.api
def test_api_get_accounts_overview(api_client: BankApiClient):
    response = api_client.get_accounts(12212)
    assert response.status_code == 200


@pytest.mark.api
def test_api_request_loan_approval(api_client: BankApiClient):
    response = api_client.request_loan(
        customer_id=12212, amount=1000.0, down_payment=100.0, from_account_id=12345
    )
    assert response.status_code == 200


@pytest.mark.api
def test_api_transfer_funds_validation(api_client: BankApiClient):
    response = api_client.transfer_funds(
        from_account_id=12345, to_account_id=12345, amount=50.0
    )
    assert response.status_code == 200