"""
Tables Page Object.
Handles interactions with Data Tables.
"""

import allure
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from config import Config


class TablesPage(BasePage):
    """Page object for /tables."""
    
    URL = f"{Config.UI_BASE_URL}/tables"
    
    HEADERS = (By.CSS_SELECTOR, "#table1 thead th span")
    
    @allure.step("Loading Tables page")
    def load(self) -> "TablesPage":
        """Opens the tables page."""
        self.open(self.URL)
        return self

    def _get_column_index(self, column_name: str) -> int:
        """
        Finds the 1-based index of a column by its header text.
        
        Args:
            column_name: Name of the column header to find
            
        Returns:
            int: 1-based column index
            
        Raises:
            ValueError: If column is not found in table
        """
        # Wait until at least one header is visible to ensure table structure is loaded
        self.wait.until(EC.visibility_of_element_located(self.HEADERS))
        headers = self.driver.find_elements(*self.HEADERS)
        
        for i, header in enumerate(headers, 1):
            if header.text == column_name:
                return i
        
        raise ValueError(f"Column '{column_name}' not found in Table 1")

    @allure.step("Clicking column header: {column_name}")
    def click_column_header(self, column_name: str) -> None:
        """Clicks a column header by its name to trigger sorting."""
        index = self._get_column_index(column_name)
        header_locator = (By.CSS_SELECTOR, f"#table1 thead th:nth-of-type({index})")
        self.click(header_locator)

    @allure.step("Getting values for column: {column_name}")
    def get_column_values(self, column_name: str) -> List[str]:
        """
        Retrieves all text values from a specific column in Table 1.
        
        Args:
            column_name: Name of the column to extract values from
            
        Returns:
            List[str]: List of cell values in the column
        """
        index = self._get_column_index(column_name)
        cell_locator = (By.CSS_SELECTOR, f"#table1 tbody tr td:nth-of-type({index})")
        
        # Ensure that cells are present before scraping
        self.wait.until(EC.presence_of_element_located(cell_locator))
        
        return [el.text for el in self.driver.find_elements(*cell_locator)]
