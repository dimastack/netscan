import pytest
import requests

from conftest import API_TEST_URL

SCAN_OS_URL = f"{API_TEST_URL}/scan/osfingerprint"

@pytest.mark.unit
@pytest.mark.scan
def test_os_fingerprint(auth_headers):
    """Test OS fingerprinting on IP."""
    digital_ocean_ip = "178.128.95.157"
    response = requests.get(SCAN_OS_URL, headers=auth_headers, params={"ip": digital_ocean_ip})
    assert response.status_code == 200
    data = response.json()
    assert data['ip'] == digital_ocean_ip
    assert data['os_guess'] == "Linux/Unix"
    assert data['packet_size'] >= 40
    assert data['ttl'] == 63
