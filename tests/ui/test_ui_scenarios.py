"""
UI Scenarios for login and data tables.
Validates user authentication and table sorting functionality.
"""
import pytest
import allure
from config import Config
from pages.login_page import LoginPage
from pages.tables_page import TablesPage


@allure.feature("UI Automation")
class TestUIScenarios:

    @allure.story("Login")
    @allure.title("Login Validation for user: {username}")
    @pytest.mark.parametrize("username, password, expected_msg", [
        pytest.param(
            Config.TEST_USER, Config.TEST_PASSWORD, 
            "You logged into a secure area!",
            id="success_login"
        ),
        pytest.param(
            "invalid_user", "invalid_pass", 
            "Your username is invalid!",
            id="error_invalid_creds"
        ),
        pytest.param(
            "", "", 
            "Your username is invalid!",
            id="error_empty_creds"
        ),
    ])
    def test_login(self, browser, username, password, expected_msg):
        """Validates login functionality with various credential sets."""
        login_page = LoginPage(browser)
        login_page.load()
        login_page.login(username, password)
        
        message = login_page.get_flash_message()
        assert expected_msg in message
        
    @allure.story("Tables")
    @allure.title("Sortable Data Tables Validation for column: {column_name}")
    @pytest.mark.parametrize("column_name", [
        "Last Name", 
        "First Name", 
        "Email"
    ])
    def test_sortable_data_tables(self, browser, column_name):
        """Verifies sorting functionality for different table columns."""
        page = TablesPage(browser)
        page.load()
        
        initial_values = page.get_column_values(column_name)
        
        page.click_column_header(column_name)
        
        sorted_values = page.get_column_values(column_name)
        
        expected_sorted = sorted(initial_values)
        assert sorted_values == expected_sorted, (
            f"Sorting for '{column_name}' failed. Expected {expected_sorted}, but got {sorted_values}"
        )
