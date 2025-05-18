import pytest
import requests

from conftest import API_TEST_URL, API_USER_CREDENTIALS

REGISTER_URL = f"{API_TEST_URL}/auth/register"

@pytest.mark.unit
@pytest.mark.auth
def test_register_existing_user():
    """Ensure trying to register an already existing user returns 409."""
    response = requests.post(REGISTER_URL, json=API_USER_CREDENTIALS)
    assert response.status_code == 409
    assert "error" in response.json()
