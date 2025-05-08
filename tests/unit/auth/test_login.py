import pytest
import requests


@pytest.mark.unit
@pytest.mark.auth
def test_login_with_valid_credentials(api_base_url, test_user_credentials):
    """Ensure login returns a valid JWT token for correct credentials."""
    url = f"{api_base_url}/auth/login"
    response = requests.post(url, json={
        "email": test_user_credentials["email"],
        "password": test_user_credentials["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.unit
@pytest.mark.auth
def test_login_with_invalid_credentials(api_base_url):
    """Ensure login fails with 401 for wrong password.""" 
    url = f"{api_base_url}/auth/login"
    response = requests.post(url, json={
        "email": "testuser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "error" in response.json()
