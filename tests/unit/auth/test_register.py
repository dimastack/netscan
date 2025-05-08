import pytest
import requests


@pytest.mark.unit
@pytest.mark.auth
def test_register_existing_user(api_base_url, test_user_credentials):
    """Ensure trying to register an already existing user returns 409."""
    url = f"{api_base_url}/auth/register"
    response = requests.post(url, json=test_user_credentials)
    assert response.status_code == 409
    assert "error" in response.json()
