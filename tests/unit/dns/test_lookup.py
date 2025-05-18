import pytest
import requests

from conftest import API_TEST_URL

DNS_LOOKUP_URL = f"{API_TEST_URL}/dns/lookup"

@pytest.mark.unit
@pytest.mark.dns
@pytest.mark.parametrize("record_type", ["A", "MX", "TXT"])
def test_dns_lookup_valid(auth_headers, record_type):
    """Test DNS lookup for valid domain and various record types."""
    params = {
        "domain": "example.com",
        "type": record_type,
        "dst": "8.8.8.8",
        "timeout": 2
    }
    response = requests.get(DNS_LOOKUP_URL, headers=auth_headers, params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert "answers" in json_data
    assert json_data["type"] == record_type


@pytest.mark.unit
@pytest.mark.dns
def test_dns_lookup_missing_domain(auth_headers):
    """Test DNS lookup error response when domain is missing."""
    response = requests.get(DNS_LOOKUP_URL, headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.json()
