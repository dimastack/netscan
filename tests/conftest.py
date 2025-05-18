import pytest
import requests

from config import add_options, get_options


API_TEST_URL = None
API_USER_CREDENTIALS = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword123"
}

UI_TEST_URL = None
BROWSER = None
UI_USER_CREDENTIALS = {
    "username": "uitest",
    "email": "uitest@example.com",
    "password": "testpassword123"
}

def pytest_addoption(parser):
    add_options(parser)

def pytest_configure(config):
    global API_TEST_URL, UI_TEST_URL, BROWSER
    opts = get_options(config)
    API_TEST_URL = opts["API_TEST_URL"]
    UI_TEST_URL = opts["UI_TEST_URL"]
    BROWSER = opts["BROWSER"]

@pytest.fixture(scope="session", autouse=True)
def auth_token():
    """
    Registers the user (if not exists), logs in, and returns a JWT token.
    """
    try:
        requests.post(
            f"{API_TEST_URL}/auth/register",
            json=API_USER_CREDENTIALS,
            timeout=5
        )
    except requests.exceptions.RequestException:
        pass  # Ignore if already exists

    response = requests.post(
        f"{API_TEST_URL}/auth/login",
        json={
            "email": API_USER_CREDENTIALS["email"],
            "password": API_USER_CREDENTIALS["password"]
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
