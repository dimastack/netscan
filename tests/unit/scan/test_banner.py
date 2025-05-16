import pytest
import requests


@pytest.mark.unit
@pytest.mark.scan
def test_banner_grab(api_base_url, auth_headers):
    """Test banner grabbing on a known port."""
    url = f"{api_base_url}/scan/bannergrab"
    # This is Google's mail server IP, on port 25 (SMTP)
    ip = "64.233.184.27"
    port = 25
    response = requests.get(url, headers=auth_headers, params={"ip": ip, "port": port, "timeout": 2})
    assert response.status_code == 200
    json_data = response.json()
    assert "220 mx.google.com ESMTP" in json_data["banner"]
    assert " - gsmtp" in json_data["banner"]
    assert json_data["ip"] == ip
    assert json_data["port"] == port
    assert json_data["status"] == "open"
