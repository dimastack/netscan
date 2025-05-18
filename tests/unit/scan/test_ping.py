import pytest
import requests

from conftest import API_TEST_URL

SCAN_PING_URL = f"{API_TEST_URL}/scan/ping"

@pytest.mark.unit
@pytest.mark.scan
def test_ping(auth_headers):
    """Test ping route with valid IP."""
    ip = "8.8.8.8"
    response = requests.get(SCAN_PING_URL, headers=auth_headers, params={"ip": ip})
    assert response.status_code == 200
    data = response.json()
    assert data['error'] == None
    assert data['ip'] == ip
    assert data['status'] == "up"
    assert data['reply_from'] == ip
    assert f'from {ip}' in data['raw_output']
    assert data['response_time_ms'] > 0


@pytest.mark.unit
@pytest.mark.scan
def test_ping_invalid_ip(auth_headers):   
    """Test ping route with invalid IP."""
    response = requests.get(SCAN_PING_URL, headers=auth_headers, params={"ip": "8.8."})
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "error"
    assert data['error'] == '[Errno -2] Name or service not known'


@pytest.mark.unit
@pytest.mark.scan
def test_ping_missing_ip(auth_headers):
    """Test ping route with missing IP."""
    response = requests.get(SCAN_PING_URL, headers=auth_headers)
    assert response.status_code == 400
