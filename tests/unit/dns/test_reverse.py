import pytest
import requests

from conftest import API_TEST_URL

DNS_REVERSE_URL = f"{API_TEST_URL}/dns/reverse"

@pytest.mark.unit
@pytest.mark.dns
def test_dns_reverse_valid(auth_headers):
    """Test reverse DNS lookup for a valid IP address."""
    params = {
        "ip": "4.2.2.1",
        "dst": "8.8.8.8",
        "timeout": 2
    }
    response = requests.get(DNS_REVERSE_URL, headers=auth_headers, params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["ip"] == "4.2.2.1"
    assert json_data["hostname"] == "a.resolvers.level3.net."


@pytest.mark.unit
@pytest.mark.dns
def test_dns_reverse_missing_ip(auth_headers):
    """Test reverse DNS lookup error response when IP is missing."""
    response = requests.get(DNS_REVERSE_URL, headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.json()
