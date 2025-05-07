import os
import pytest
import requests


@pytest.fixture(scope="session")
def api_base_url():
    """
    Returns the base URL for API requests.
    You can override this with the BACKEND_URL environment variable.
    """
    return os.getenv("BACKEND_URL", "http://localhost:5001/api/v1")


@pytest.fixture(scope="session")
def test_user_credentials():
    """
    Returns static test user credentials.
    Update as needed.
    """
    return {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword123"
    }


@pytest.fixture(scope="session")
def auth_token(api_base_url, test_user_credentials):
    """
    Registers the user (if not exists), logs in, and returns a JWT token.
    """
    # Try register
    try:
        requests.post(
            f"{api_base_url}/auth/register",
            json=test_user_credentials,
            timeout=5
        )
    except requests.exceptions.RequestException:
        pass  # User might already exist, ignore

    # Login
    response = requests.post(
        f"{api_base_url}/auth/login",
        json={
            "email": test_user_credentials["email"],
            "password": test_user_credentials["password"]
        }
    )
    response.raise_for_status()
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """
    Returns a dict with Authorization header.
    """
    return {
        "Authorization": f"Bearer {auth_token}"
    }
