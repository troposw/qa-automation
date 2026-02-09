"""
Base Page module.
Contains methods common to all Page Objects.
"""

import allure
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple
from config import Config


class BasePage:
    """Base class for all Page Objects."""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, Config.TIMEOUT, poll_frequency=Config.POLL_FREQUENCY)

    @allure.step("Opening URL: {url}")
    def open(self, url: str) -> None:
        """Opens the specified URL."""
        self.driver.get(url)

    @allure.step("Finding element: {locator}")
    def find(self, locator: Tuple[str, str]) -> WebElement:
        """
        Waits for an element to be visible and returns it.
        
        Args:
            locator: Tuple (By.ID, "value")
            
        Returns:
            WebElement: The visible element
        """
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step("Clicking on element: {locator}")
    def click(self, locator: Tuple[str, str]) -> None:
        """
        Waits for an element to be clickable and clicks it.
        
        Args:
            locator: Tuple (By.ID, "value")
        """
        element: WebElement = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    @allure.step("Getting text from element: {locator}")
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Waits for an element to be visible and returns its text.
        
        Args:
            locator: Tuple (By.ID, "value")
            
        Returns:
            str: Text content of the element
        """
        return self.find(locator).text
