"""
API Client module.
Wrapper around the requests library for easier API testing.
"""

import allure
import requests
from requests import Response
from typing import Optional, Dict, Any
from config import Config


class ApiClient:
    """
    Wrapper class for making HTTP requests using a persistent session.
    
    Provides methods for GET, POST, PUT, PATCH, DELETE with automatic timeout
    and optional logging. Supports context manager usage.
    """

    def __init__(self, base_url: str, default_headers: Optional[Dict[str, str]] = None):
        """
        Initialize API client with base URL and optional default headers.
        
        Args:
            base_url: Base URL for all requests
            default_headers: Optional dict of headers to include in all requests
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = Config.TIMEOUT
        
        if default_headers:
            self.session.headers.update(default_headers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Closes the underlying session."""
        self.session.close()

    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        """
        Internal method for unified request handling.
        
        Args:
            method: HTTP method (GET, POST, PUT, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            Response object
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        kwargs.setdefault('timeout', self.timeout)
        
        # Execute the request
        return self.session.request(method, url, **kwargs)

    @allure.step("GET {endpoint}")
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        """
        Sends a GET request.
        
        Args:
            endpoint: API endpoint
            params: Optional query parameters
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._request('GET', endpoint, params=params, **kwargs)

    @allure.step("POST {endpoint}")
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
             json: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        """
        Sends a POST request.
        
        Args:
            endpoint: API endpoint
            data: Optional form data
            json: Optional JSON payload
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._request('POST', endpoint, data=data, json=json, **kwargs)

    @allure.step("PUT {endpoint}")
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
            json: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        """
        Sends a PUT request.
        
        Args:
            endpoint: API endpoint
            data: Optional form data
            json: Optional JSON payload
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._request('PUT', endpoint, data=data, json=json, **kwargs)

    @allure.step("PATCH {endpoint}")
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None, 
              json: Optional[Dict[str, Any]] = None, **kwargs) -> Response:
        """
        Sends a PATCH request.
        
        Args:
            endpoint: API endpoint
            data: Optional form data
            json: Optional JSON payload
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._request('PATCH', endpoint, data=data, json=json, **kwargs)

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str, **kwargs) -> Response:
        """
        Sends a DELETE request.
        
        Args:
            endpoint: API endpoint
            **kwargs: Additional arguments
            
        Returns:
            Response object
        """
        return self._request('DELETE', endpoint, **kwargs)
