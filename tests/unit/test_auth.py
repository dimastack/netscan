import requests


def test_register_existing_user(api_base_url, test_user_credentials):
    """Ensure trying to register an already existing user returns 409."""
    url = f"{api_base_url}/auth/register"
    response = requests.post(url, json=test_user_credentials)
    assert response.status_code == 409
    assert "error" in response.json()


def test_login_with_valid_credentials(api_base_url, test_user_credentials):
    """Ensure login returns a valid JWT token for correct credentials."""
    url = f"{api_base_url}/auth/login"
    response = requests.post(url, json={
        "email": test_user_credentials["email"],
        "password": test_user_credentials["password"]
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_invalid_credentials(api_base_url):
    """Ensure login fails with 401 for wrong password.""" 
    url = f"{api_base_url}/auth/login"
    response = requests.post(url, json={
        "email": "testuser@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "error" in response.json()


def test_me_endpoint(api_base_url, auth_headers):
    """Ensure /auth/me returns current user ID with valid token."""
    url = f"{api_base_url}/auth/me"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 200
    assert "user_id" in response.json()
