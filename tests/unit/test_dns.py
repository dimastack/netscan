import pytest
import requests


@pytest.mark.parametrize("record_type", ["A", "MX", "TXT"])
def test_dns_lookup_valid(api_base_url, auth_headers, record_type):
    """Test DNS lookup for valid domain and various record types."""
    params = {
        "domain": "example.com",
        "type": record_type,
        "dst": "8.8.8.8",
        "timeout": 2
    }
    url = f"{api_base_url}/dns/lookup"
    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert "answers" in json_data
    assert json_data["type"] == record_type


def test_dns_lookup_missing_domain(api_base_url, auth_headers):
    """Test DNS lookup error response when domain is missing."""
    url = f"{api_base_url}/dns/lookup"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.json()


def test_dns_reverse_valid(api_base_url, auth_headers):
    """Test reverse DNS lookup for a valid IP address."""
    params = {
        "ip": "8.8.8.8",
        "dst": "8.8.8.8",
        "timeout": 2
    }
    url = f"{api_base_url}/dns/reverse"
    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["ip"] == "8.8.8.8"
    assert "hostname" in json_data


def test_dns_reverse_missing_ip(api_base_url, auth_headers):
    """Test reverse DNS lookup error response when IP is missing."""
    url = f"{api_base_url}/dns/reverse"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.json()


def test_whois_lookup_valid(api_base_url, auth_headers):
    """Test WHOIS lookup for a valid domain."""
    params = {"domain": "example.com"}
    url = f"{api_base_url}/dns/whois"
    response = requests.get(url, headers=auth_headers, params=params)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["domain"] == "example.com"
    assert "registrar" in json_data


def test_whois_lookup_missing_domain(api_base_url, auth_headers):
    """Test WHOIS lookup error response when domain is missing."""
    url = f"{api_base_url}/dns/whois"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 400
    assert "error" in response.json()
