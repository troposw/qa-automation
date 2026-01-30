"""
API Scenarios for HTTP methods.
Validates core HTTP methods (GET, POST, etc.) and payload handling.
"""
import pytest
import allure
from config import Config
from api.client import ApiClient


@allure.feature("API Automation")
@allure.tag("api")
class TestApiScenarios:

    @pytest.fixture(autouse=True)
    def setup(self):
        """Initializes API client and handles cleanup."""
        self.api = ApiClient(Config.API_BASE_URL)
        yield
        self.api.close()

    @allure.story("HTTP Methods")
    @allure.title("GET Request Validation")
    def test_get_request(self):
        """Validates that a GET request returns JSON content."""
        response = self.api.get("get")
        assert response.status_code == 200
        assert "application/json" in response.headers["Content-Type"]

    @allure.story("HTTP Methods")
    @allure.title("POST Request Validation with payload: {payload}")
    @pytest.mark.parametrize("payload", [
        pytest.param({"name": "QA Candidate", "role": "Senior Engineer"}, id="full_data"),
        pytest.param({"name": "Only Name"}, id="partial_data"),
        pytest.param({}, id="empty_data"),
    ])
    def test_post_request(self, payload):
        """Validates POST functionality with various JSON payloads."""
        response = self.api.post("post", json=payload)
        assert response.status_code == 200
        response_json = response.json()
        assert response_json["json"] == payload, (
            f"Expected {payload}, but the API returned {response_json.get('json')}"
        )
