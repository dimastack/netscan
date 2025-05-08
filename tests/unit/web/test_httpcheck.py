import pytest
import requests


@pytest.mark.unit
@pytest.mark.web
def test_http_check(api_base_url, auth_headers):
    """
    Test basic HTTP check for a valid URL.
    Should return status code, headers, redirect info, etc.
    """
    url = f"{api_base_url}/web/httpcheck"
    response = requests.get(url, headers=auth_headers, params={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "status_code" in data
    assert "headers" in data
    assert "url" in data
