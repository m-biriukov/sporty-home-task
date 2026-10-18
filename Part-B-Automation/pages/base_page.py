import logging
import re

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.relative_locator import RelativeBy
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger("driver")

ByType = str | By | RelativeBy
_http_regular = re.compile(r"^https?://.*")


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url

    def open(self, url: str | None = None):
        url = url or ""
        if not _http_regular.match(url):
            url = f"{self.base_url}{url}"
        logger.info(f"Opening URL: {url}")
        self.driver.get(url)

    def find_element(
        self, by: ByType = By.ID, value: str | None = None
    ) -> WebElement:
        logger.info(f"Searching element by {by} '{value}'")
        return self.driver.find_element(by, value)

    def find_elements(
        self, by: ByType = By.ID, value: str | None = None
    ) -> list[WebElement]:
        logger.info(f"Searching elements by {by} '{value}'")
        result = self.driver.find_elements(by, value)
        logger.info(f"Found {len(result)} webelements")
        return result

    def click(self, by: ByType = By.ID, value: str | None = None):
        logger.info(f"Click element by {by} '{value}'")
        self.driver.find_element(by, value).click()

    def get_text(self, by: ByType = By.ID, value: str | None = None) -> str:
        logger.info(f"Getting text by {by} '{value}'")
        return self.driver.find_element(by, value).text

    def _wait_for(self, condition, timeout: int) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(condition)
            return True
        except TimeoutException:
            return False

    def is_visible(
        self, by: ByType = By.ID, value: str | None = None, timeout: int = 10
    ) -> bool:
        return self._wait_for(
            EC.visibility_of_element_located((by, value)), timeout
        )

    def is_invisible(
        self, by: ByType = By.ID, value: str | None = None, timeout: int = 10
    ) -> bool:
        return self._wait_for(
            EC.invisibility_of_element_located((by, value)), timeout
        )

    def wait_to_be_visible(
        self, by: ByType = By.ID, value: str | None = None, timeout: int = 10
    ):
        logger.info(f"Waiting to be visible by {by} '{value}'")
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.presence_of_element_located((by, value)))
        wait.until(EC.visibility_of(element))

    def wait_to_have_text(
        self,
        by: ByType = By.ID,
        value: str | None = None,
        text: str = "",
        timeout: int = 10,
    ):
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element((by, value), text)
        )
