import pytest
import requests

from conftest import API_TEST_URL, API_USER_CREDENTIALS

LOGIN_URL = f"{API_TEST_URL}/auth/login"

@pytest.mark.unit
@pytest.mark.auth
def test_login_with_valid_credentials():
    """Ensure login returns a valid JWT token for correct credentials."""
    response = requests.post(LOGIN_URL, json={
        "email": API_USER_CREDENTIALS["email"],
        "password": API_USER_CREDENTIALS["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.unit
@pytest.mark.auth
def test_login_with_invalid_credentials():
    """Ensure login fails with 401 for wrong password.""" 
    response = requests.post(LOGIN_URL, json={
        "email": "testuser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "error" in response.json()
