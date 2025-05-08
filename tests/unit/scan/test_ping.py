import pytest
import requests


@pytest.mark.unit
@pytest.mark.scan
def test_ping(api_base_url, auth_headers):
    """Test ping route with valid IP."""
    url = f"{api_base_url}/scan/ping"
    ip = "8.8.8.8"
    response = requests.get(url, headers=auth_headers, params={"ip": ip})
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
def test_ping_invalid_ip(api_base_url, auth_headers):   
    """Test ping route with invalid IP."""
    url = f"{api_base_url}/scan/ping"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8."})
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "error"
    assert data['error'] == '[Errno -2] Name or service not known'


@pytest.mark.unit
@pytest.mark.scan
def test_ping_missing_ip(api_base_url, auth_headers):
    """Test ping route with missing IP."""
    url = f"{api_base_url}/scan/ping"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 400
