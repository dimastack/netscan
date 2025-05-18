import pytest
import requests

from conftest import API_TEST_URL

SCAN_TRACE_URL = f"{API_TEST_URL}/scan/traceroute"

@pytest.mark.unit
@pytest.mark.scan
def test_trace(auth_headers):
    """Test traceroute functionality."""
    response = requests.get(SCAN_TRACE_URL, 
                            headers=auth_headers, 
                            params={"ip": "8.8.8.8"})
    assert response.status_code == 200
    data = response.json()
    assert data['error'] == None
    assert data['hops'][0]['status'] == 'ok'
    assert '172.' in data['hops'][0]['ip']
