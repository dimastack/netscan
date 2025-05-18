import pytest
import requests

from conftest import API_TEST_URL

UTILS_HEADERS_URL = f"{API_TEST_URL}/utils/headers"

@pytest.mark.unit
@pytest.mark.utils
def test_http_headers(auth_headers):
    """Test HTTP headers retrieval for a valid URL."""
    response = requests.get(UTILS_HEADERS_URL, 
                            headers=auth_headers, 
                            params={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "Server" in data or isinstance(data, dict)
