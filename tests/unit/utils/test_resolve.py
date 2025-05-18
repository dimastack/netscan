import pytest
import requests
import re

from conftest import API_TEST_URL

UTILS_RESOLVE_URL = f"{API_TEST_URL}/utils/resolve"

@pytest.mark.unit
@pytest.mark.utils
def test_resolve_hostname(auth_headers):
    """Test hostname resolution for a valid host."""
    hostname = "example.com"
    response = requests.get(UTILS_RESOLVE_URL, 
                            headers=auth_headers, 
                            params={"host": hostname})
    assert response.status_code == 200
    data = response.json()
    assert data['hostname'] == hostname
    re_ip = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    assert re_ip.match(data['ip'])
    assert data['error'] == None
