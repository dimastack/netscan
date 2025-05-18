import pytest
import requests

from conftest import API_TEST_URL

WEB_SSL_URL = f"{API_TEST_URL}/web/sslcheck"


@pytest.mark.unit
@pytest.mark.web
def test_ssl_check(auth_headers):
    """
    Test SSL certificate details for a valid HTTPS host.
    Should return subject, issuer, expiration dates, etc.
    """
    response = requests.get(WEB_SSL_URL, 
                            headers=auth_headers, 
                            params={"url": "https://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "hostname" in data
    assert "valid_to" in data
    assert "issuer" in data or "subject" in data
