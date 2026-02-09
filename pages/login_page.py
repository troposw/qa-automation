"""
Login Page Object.
Handles interactions with the login form.
"""

import allure
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import Config


class LoginPage(BasePage):
    """Page object for /login."""
    
    URL = f"{Config.UI_BASE_URL}/login"
    
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")

    @allure.step("Loading Login page")
    def load(self) -> "LoginPage":
        self.open(self.URL)
        return self

    @allure.step("Logging in with username: {username}")
    def login(self, username: str, password: str) -> None:
        """Performs login action."""
        self.find(self.USERNAME_INPUT).send_keys(username)
        self.find(self.PASSWORD_INPUT).send_keys(password)
        self.click(self.LOGIN_BUTTON)

    def get_flash_message(self) -> str:
        """Returns the text of the flash message (alert)."""
        return self.get_text(self.FLASH_MESSAGE)
