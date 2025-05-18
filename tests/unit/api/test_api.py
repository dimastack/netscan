import pytest
import requests

from conftest import API_TEST_URL


@pytest.mark.unit
@pytest.mark.api
def test_api_index(request):
    """Check that API index is accessible and returns expected content."""
    response = requests.get(f"{API_TEST_URL}/")
    assert response.status_code == 200
    assert "message" in response.json()
