import pytest
import requests

from conftest import API_TEST_URL

ME_URL = f"{API_TEST_URL}/auth/me"

@pytest.mark.unit
@pytest.mark.auth
def test_me_endpoint(auth_headers):
    """Ensure /auth/me returns current user ID with valid token."""
    response = requests.get(ME_URL, headers=auth_headers)
    assert response.status_code == 200
    assert "user_id" in response.json()
