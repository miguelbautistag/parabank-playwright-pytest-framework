import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://parabank.parasoft.com/parabank").rstrip("/")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://parabank.parasoft.com/parabank/services/bank").rstrip("/")
    DEFAULT_TIMEOUT: int = int(os.getenv("DEFAULT_TIMEOUT", "10000"))
    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
