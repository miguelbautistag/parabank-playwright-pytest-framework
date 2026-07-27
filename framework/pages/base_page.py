from urllib.parse import urljoin
from playwright.sync_api import Page
from config.settings import Config
from framework.utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def navigate(self, path: str = "") -> None:
        relative_path = path.lstrip("/")
        url = f"{Config.BASE_URL}/{relative_path}" if relative_path else Config.BASE_URL
        self.logger.info(f"Navigating to {url}")
        self.page.goto(url)

    def wait_for_url_contains(self, partial_url: str) -> None:
        self.page.wait_for_url(f"**/{partial_url}**", timeout=Config.DEFAULT_TIMEOUT)