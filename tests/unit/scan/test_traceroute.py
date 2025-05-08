import pytest
import requests


@pytest.mark.unit
@pytest.mark.scan
def test_trace(api_base_url, auth_headers):
    """Test traceroute functionality."""
    url = f"{api_base_url}/scan/trace"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8"})
    assert response.status_code == 200
    data = response.json()
    assert data['error'] == None
    assert data['hops'][0]['status'] == 'ok'
    assert '172.' in data['hops'][0]['ip']
