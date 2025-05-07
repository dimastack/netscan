import requests

def test_api_index(api_base_url):
    """Check that API index is accessible and returns expected content."""
    import pdb;pdb.set_trace
    response = requests.get(f"{api_base_url}/")
    assert response.status_code == 200
    assert "message" in response.json()
