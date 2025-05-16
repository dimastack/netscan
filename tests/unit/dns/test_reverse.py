import pytest
import requests


@pytest.mark.unit
@pytest.mark.dns
def test_dns_reverse_valid(api_base_url, auth_headers):
    """Test reverse DNS lookup for a valid IP address."""
    params = {
        "ip": "4.2.2.1",
        "dst": "8.8.8.8",
        "timeout": 2
    }
    url = f"{api_base_url}/dns/reverse"
    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["ip"] == "4.2.2.1"
    assert json_data["hostname"] == "a.resolvers.level3.net."


@pytest.mark.unit
@pytest.mark.dns
def test_dns_reverse_missing_ip(api_base_url, auth_headers):
    """Test reverse DNS lookup error response when IP is missing."""
    url = f"{api_base_url}/dns/reverse"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.json()
