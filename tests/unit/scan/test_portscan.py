import pytest
import requests

from conftest import API_TEST_URL

SCAN_SYN_URL = f"{API_TEST_URL}/scan/synscan"
SCAN_TCP_CON_URL = f"{API_TEST_URL}/scan/tcpconnect"
SCAN_UDP_URL = f"{API_TEST_URL}/scan/udp"
SCAN_PORTS_URL = f"{API_TEST_URL}/scan/portscan"

@pytest.mark.unit
@pytest.mark.scan
def test_syn_scan(auth_headers):
    """Test SYN scan for multiple ports."""
    response = requests.get(SCAN_SYN_URL, 
                            headers=auth_headers, 
                            params={"ip": "8.8.8.8", "ports": "22,80"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.unit
@pytest.mark.scan
def test_tcp_connect(auth_headers):
    """Test TCP connect scan for a common open port."""
    response = requests.get(SCAN_TCP_CON_URL, 
                            headers=auth_headers, 
                            params={"ip": "8.8.8.8", "port": 80})
    assert response.status_code == 200
    assert "status" in response.json()


@pytest.mark.unit
@pytest.mark.scan
def test_udp_scan(auth_headers):
    """Test UDP scan with one port."""
    response = requests.get(SCAN_UDP_URL, 
                            headers=auth_headers, 
                            params={"ip": "8.8.8.8", "ports": "21,53"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


@pytest.mark.unit
@pytest.mark.scan
def test_portscan_range(auth_headers):
    """Test full port scan range from 1-100."""
    response = requests.get(SCAN_PORTS_URL, 
                            headers=auth_headers, 
                            params={"ip": "8.8.8.8", "range": "1-100"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
