import pytest
import requests


@pytest.mark.unit
@pytest.mark.dns
def test_whois_lookup_valid(api_base_url, auth_headers):
    """Test WHOIS lookup for a valid domain."""
    params = {"domain": "example.com"}
    url = f"{api_base_url}/dns/whois"
    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["domain"] == "example.com"
    assert "registrar" in json_data


@pytest.mark.unit
@pytest.mark.dns
def test_whois_lookup_missing_domain(api_base_url, auth_headers):
    """Test WHOIS lookup error response when domain is missing."""
    url = f"{api_base_url}/dns/whois"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.json()
