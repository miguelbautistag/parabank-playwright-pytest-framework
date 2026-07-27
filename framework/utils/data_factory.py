import uuid
from faker import Faker

faker = Faker()


class DataFactory:
    """
    Generates dynamic, parallel-safe test payloads for API and UI testing layers.
    Appends short UUID slices to guarantee zero data collisions under pytest-xdist execution.
    """

    @staticmethod
    def create_user_payload() -> dict:
        unique_id = uuid.uuid4().hex[:8]
        username = f"user_{unique_id}"

        return {
            "firstName": faker.first_name(),
            "lastName": faker.last_name(),
            "street": faker.street_address(),
            "city": faker.city(),
            "state": faker.state(),
            "zipCode": faker.zipcode(),
            "phoneNumber": "555-019-2834",
            "ssn": faker.ssn(),
            "username": username,
            "password": "Password123!",
        }

    @staticmethod
    def create_bill_pay_payload() -> dict:
        payee_company = faker.company()
        acct_num = "12345"

        return {
            "name": payee_company,
            "address": faker.street_address(),
            "city": faker.city(),
            "state": faker.state(),
            "zipCode": faker.zipcode(),
            "phone": "555-019-2834",
            "account": acct_num,
            "amount": "100",
        }