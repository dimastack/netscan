import pytest
import requests


@pytest.mark.unit
@pytest.mark.utils
def test_check_latency(api_base_url, auth_headers):
    """Test latency check for host:port."""
    url = f"{api_base_url}/utils/latency"
    host = "example.com"
    port = 80
    response = requests.get(url, headers=auth_headers, params={"host": host, "port": port})
    assert response.status_code == 200
    data = response.json()
    data['error'] == None
    assert data['host'] == host
    assert data['port'] == port
    assert data['status'] == "online"
    assert data['latency_ms'] > 0
