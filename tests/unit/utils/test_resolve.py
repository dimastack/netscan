import pytest
import requests
import re


@pytest.mark.unit
@pytest.mark.utils
def test_resolve_hostname(api_base_url, auth_headers):
    """Test hostname resolution for a valid host."""
    url = f"{api_base_url}/utils/resolve"
    hostname = "example.com"
    response = requests.get(url, headers=auth_headers, params={"host": hostname})
    assert response.status_code == 200
    data = response.json()
    assert data['hostname'] == hostname
    re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    assert re_ip.match(data['ip'])
    assert data['error'] == None


@pytest.mark.unit
@pytest.mark.utils
def test_reverse_dns(api_base_url, auth_headers):
    """Test reverse DNS resolution for a valid IP."""
    url = f"{api_base_url}/utils/reverse"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8"})
    assert response.status_code == 200
    assert "hostname" in response.json()
