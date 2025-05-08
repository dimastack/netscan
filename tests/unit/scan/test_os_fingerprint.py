import pytest
import requests


@pytest.mark.unit
@pytest.mark.scan
def test_os_fingerprint(api_base_url, auth_headers):
    """Test OS fingerprinting on IP."""
    url = f"{api_base_url}/scan/osfingerprint"
    digital_ocean_ip = "178.128.95.157"
    response = requests.get(url, headers=auth_headers, params={"ip": digital_ocean_ip})
    assert response.status_code == 200
    data = response.json()
    assert data['ip'] == digital_ocean_ip
    assert data['os_guess'] == "Linux/Unix"
    assert data['packet_size'] == 40
    assert data['ttl'] == 63
