import pytest
import requests
import re

from conftest import API_TEST_URL

UTILS_REVERSE_URL = f"{API_TEST_URL}/utils/reverse"

@pytest.mark.unit
@pytest.mark.utils
def test_reverse_dns(auth_headers):
    """Test reverse DNS resolution for a valid IP."""
    ip = "8.8.8.8"
    response = requests.get(UTILS_REVERSE_URL, 
                            headers=auth_headers, 
                            params={"ip": ip})
    assert response.status_code == 200
    data = response.json()
    assert data['ip'] == ip
    assert data['hostname'] == "dns.google"