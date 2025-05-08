import pytest
import requests


@pytest.mark.unit
@pytest.mark.scan
def test_syn_scan(api_base_url, auth_headers):
    """Test SYN scan for multiple ports."""
    url = f"{api_base_url}/scan/synscan"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "ports": "22,80"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.unit
@pytest.mark.scan
def test_tcp_connect(api_base_url, auth_headers):
    """Test TCP connect scan for a common open port."""
    url = f"{api_base_url}/scan/tcpconnect"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "port": 80})
    assert response.status_code == 200
    assert "status" in response.json()


@pytest.mark.unit
@pytest.mark.scan
def test_udp_scan(api_base_url, auth_headers):
    """Test UDP scan with one port."""
    url = f"{api_base_url}/scan/udp"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "port": 53})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.unit
@pytest.mark.scan
def test_portscan_range(api_base_url, auth_headers):
    """Test full port scan range from 1-100."""
    url = f"{api_base_url}/scan/portscan"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "range": "1-100"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
