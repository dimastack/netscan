import pytest
import requests

from conftest import API_TEST_URL

UTILS_LATENCY_URL = f"{API_TEST_URL}/utils/latency"


@pytest.mark.unit
@pytest.mark.utils
def test_check_latency(auth_headers):
    """Test latency check for host:port."""
    host = "example.com"
    port = 80
    response = requests.get(UTILS_LATENCY_URL, 
                            headers=auth_headers, 
                            params={"host": host, "port": port})
    assert response.status_code == 200
    data = response.json()
    data['error'] == None
    assert data['host'] == host
    assert data['port'] == port
    assert data['status'] == "online"
    assert data['latency_ms'] > 0
