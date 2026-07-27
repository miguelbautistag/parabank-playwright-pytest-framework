import requests
from typing import Optional
from config.settings import Config
from framework.utils.logger import get_logger

logger = get_logger("BankApiClient")


class BankApiClient:
    """
    Isolated REST API Service Client for ParaBank.
    Encapsulates HTTP request execution, parameter serialization, and endpoint routing.
    """

    def __init__(self, base_url: str = Config.API_BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

    def get_customer_details(self, customer_id: int) -> requests.Response:
        url = f"{self.base_url}/customers/{customer_id}"
        logger.info(f"GET Request to: {url}")
        return self.session.get(url)

    def get_accounts(self, customer_id: int) -> requests.Response:
        url = f"{self.base_url}/customers/{customer_id}/accounts"
        logger.info(f"GET Request to: {url}")
        return self.session.get(url)

    def create_account(
        self, customer_id: int, new_account_type: int, from_account_id: int
    ) -> requests.Response:
        url = f"{self.base_url}/createAccount"
        params = {
            "customerId": customer_id,
            "newAccountType": new_account_type,
            "fromAccountId": from_account_id,
        }
        logger.info(f"POST Request to: {url} with params: {params}")
        return self.session.post(url, params=params)

    def transfer_funds(
        self, from_account_id: int, to_account_id: int, amount: float
    ) -> requests.Response:
        url = f"{self.base_url}/transfer"
        params = {
            "fromAccountId": from_account_id,
            "toAccountId": to_account_id,
            "amount": amount,
        }
        logger.info(f"POST Request to: {url} with params: {params}")
        return self.session.post(url, params=params)

    def request_loan(
        self, customer_id: int, amount: float, down_payment: float, from_account_id: int
    ) -> requests.Response:
        url = f"{self.base_url}/requestLoan"
        params = {
            "customerId": customer_id,
            "amount": amount,
            "downPayment": down_payment,
            "fromAccountId": from_account_id,
        }
        logger.info(f"POST Request to: {url} with params: {params}")
        return self.session.post(url, params=params)