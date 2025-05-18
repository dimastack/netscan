import pytest
import requests

from conftest import API_TEST_URL

DNS_WHOIS_URL = f"{API_TEST_URL}/dns/whois"

@pytest.mark.unit
@pytest.mark.dns
def test_whois_lookup_valid(auth_headers):
    """Test WHOIS lookup for a valid domain."""
    params = {"domain": "example.com"}
    response = requests.get(DNS_WHOIS_URL, headers=auth_headers, params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["domain"] == "example.com"
    assert "registrar" in json_data


@pytest.mark.unit
@pytest.mark.dns
def test_whois_lookup_missing_domain(auth_headers):
    """Test WHOIS lookup error response when domain is missing."""
    response = requests.get(DNS_WHOIS_URL, headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.json()
