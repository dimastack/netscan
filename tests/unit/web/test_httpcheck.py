import pytest
import requests

from conftest import API_TEST_URL

WEB_HTTP_URL = f"{API_TEST_URL}/web/httpcheck"


@pytest.mark.unit
@pytest.mark.web
def test_http_check(auth_headers):
    """
    Test basic HTTP check for a valid URL.
    Should return status code, headers, redirect info, etc.
    """
    response = requests.get(WEB_HTTP_URL, 
                            headers=auth_headers, 
                            params={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "status_code" in data
    assert "headers" in data
    assert "url" in data
