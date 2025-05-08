import pytest
import requests


@pytest.mark.unit
@pytest.mark.web
def test_ssl_check(api_base_url, auth_headers):
    """
    Test SSL certificate details for a valid HTTPS host.
    Should return subject, issuer, expiration dates, etc.
    """
    url = f"{api_base_url}/web/sslcheck"
    response = requests.get(url, headers=auth_headers, params={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "hostname" in data
    assert "valid_to" in data
    assert "issuer" in data or "subject" in data
