import pytest
import requests


@pytest.mark.unit
@pytest.mark.utils
def test_http_headers(api_base_url, auth_headers):
    """Test HTTP headers retrieval for a valid URL."""
    url = f"{api_base_url}/utils/headers"
    response = requests.get(url, headers=auth_headers, params={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "Server" in data or isinstance(data, dict)
