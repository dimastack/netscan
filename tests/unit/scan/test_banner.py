import pytest
import requests

from conftest import API_TEST_URL

SCAN_BANNER_URL = f"{API_TEST_URL}/scan/bannergrab"

@pytest.mark.unit
@pytest.mark.scan
def test_banner_grab(auth_headers):
    """Test banner grabbing on a known port."""
    # This is Google's mail server IP, on port 25 (SMTP)
    ip = "64.233.184.27"
    port = 25
    response = requests.get(SCAN_BANNER_URL, 
                            headers=auth_headers, 
                            params={"ip": ip, "port": port, "timeout": 2})
    assert response.status_code == 200
    json_data = response.json()
    assert "220 mx.google.com ESMTP" in json_data["banner"]
    assert " - gsmtp" in json_data["banner"]
    assert json_data["ip"] == ip
    assert json_data["port"] == port
    assert json_data["status"] == "open"
