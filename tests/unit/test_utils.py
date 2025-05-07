import requests
import re


def test_resolve_hostname(api_base_url, auth_headers):
    """Test hostname resolution for a valid host."""
    url = f"{api_base_url}/utils/resolve"
    hostname = "example.com"
    response = requests.get(url, headers=auth_headers, params={"host": hostname})
    assert response.status_code == 200
    data = response.json()
    assert data['hostname'] == hostname
    re_ip = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
    assert re_ip.match(data['ip'])
    assert data['error'] == None


def test_reverse_dns(api_base_url, auth_headers):
    """Test reverse DNS resolution for a valid IP."""
    url = f"{api_base_url}/utils/reverse"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8"})
    assert response.status_code == 200
    assert "hostname" in response.json()


def test_check_latency(api_base_url, auth_headers):
    """Test latency check for host:port."""
    url = f"{api_base_url}/utils/latency"
    host = "example.com"
    port = 80
    response = requests.get(url, headers=auth_headers, params={"host": host, "port": port})
    assert response.status_code == 200
    data = response.json()
    data['error'] == None
    assert data['host'] == host
    assert data['port'] == port
    assert data['status'] == "online"
    assert data['latency_ms'] > 0


def test_http_headers(api_base_url, auth_headers):
    """Test HTTP headers retrieval for a valid URL."""
    url = f"{api_base_url}/utils/headers"
    response = requests.get(url, headers=auth_headers, params={"url": "http://example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "Server" in data or isinstance(data, dict)
