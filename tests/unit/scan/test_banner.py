import pytest
import requests


@pytest.mark.unit
@pytest.mark.scan
def test_banner_grab(api_base_url, auth_headers):
    """Test banner grabbing on a known port."""
    url = f"{api_base_url}/scan/bannergrab"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "port": 80})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
