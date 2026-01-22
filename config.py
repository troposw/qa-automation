"""
Configuration management for UI and API tests.
Prioritizes system environment variables over .env file.
"""
import os
from pathlib import Path
from typing import Any
from dotenv import load_dotenv

# Load .env file if it exists (local development)
load_dotenv(Path(__file__).parent / ".env")

def get_env(key: str, default: Any, cast_type: type = str) -> Any:
    """Helper to get and cast environment variables."""
    value = os.getenv(key)
    if value is None:
        return default
    if cast_type == bool:
        return value.lower() in ("true", "1", "yes", "on")
    try:
        return cast_type(value)
    except (ValueError, TypeError):
        return default

class Config:
    """Base configuration class."""
    
    # Base URLs
    UI_BASE_URL = get_env("UI_BASE_URL", "https://the-internet.herokuapp.com")
    API_BASE_URL = get_env("API_BASE_URL", "https://httpbin.org")
    
    # Test Credentials
    TEST_USER = get_env("TEST_USER", "tomsmith")
    TEST_PASSWORD = get_env("TEST_PASSWORD", "SuperSecretPassword!")
    
    # Timeout Configuration
    TIMEOUT = get_env("TIMEOUT", 10, int)
    POLL_FREQUENCY = get_env("POLL_FREQUENCY", 0.5, float)
    
    # Browser Configuration
    HEADLESS = get_env("HEADLESS", False, bool)
