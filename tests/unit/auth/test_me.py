import pytest
import requests


@pytest.mark.unit
@pytest.mark.auth
def test_me_endpoint(api_base_url, auth_headers):
    """Ensure /auth/me returns current user ID with valid token."""
    url = f"{api_base_url}/auth/me"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 200
    assert "user_id" in response.json()
