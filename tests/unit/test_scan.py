import requests


def test_ping(api_base_url, auth_headers):
    """Test ping route with valid IP."""
    url = f"{api_base_url}/scan/ping"
    ip = "8.8.8.8"
    response = requests.get(url, headers=auth_headers, params={"ip": ip})
    assert response.status_code == 200
    data = response.json()
    assert data['error'] == None
    assert data['ip'] == ip
    assert data['status'] == "up"
    assert data['reply_from'] == ip
    assert f'from {ip}' in data['raw_output']
    assert data['response_time_ms'] > 0


def test_ping_invalid_ip(api_base_url, auth_headers):   
    """Test ping route with invalid IP."""
    url = f"{api_base_url}/scan/ping"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8."})
    assert response.status_code == 200
    data = response.json()
    assert data['status'] == "error"
    assert data['error'] == '[Errno -2] Name or service not known'


def test_ping_missing_ip(api_base_url, auth_headers):
    """Test ping route with missing IP."""
    url = f"{api_base_url}/scan/ping"
    response = requests.get(url, headers=auth_headers)
    assert response.status_code == 400


def test_trace(api_base_url, auth_headers):
    """Test traceroute functionality."""
    url = f"{api_base_url}/scan/trace"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8"})
    assert response.status_code == 200
    data = response.json()
    assert data['error'] == None
    assert data['hops'][0]['status'] == 'ok'
    assert '172.' in data['hops'][0]['ip']


def test_syn_scan(api_base_url, auth_headers):
    """Test SYN scan for multiple ports."""
    url = f"{api_base_url}/scan/synscan"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "ports": "22,80"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_tcp_connect(api_base_url, auth_headers):
    """Test TCP connect scan for a common open port."""
    url = f"{api_base_url}/scan/tcpconnect"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "port": 80})
    assert response.status_code == 200
    assert "status" in response.json()


def test_udp_scan(api_base_url, auth_headers):
    """Test UDP scan with one port."""
    url = f"{api_base_url}/scan/udp"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "port": 53})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_portscan_range(api_base_url, auth_headers):
    """Test full port scan range from 1-100."""
    url = f"{api_base_url}/scan/portscan"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "range": "1-100"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_os_fingerprint(api_base_url, auth_headers):
    """Test OS fingerprinting on IP."""
    url = f"{api_base_url}/scan/osfingerprint"
    digital_ocean_ip = "178.128.95.157"
    response = requests.get(url, headers=auth_headers, params={"ip": digital_ocean_ip})
    assert response.status_code == 200
    data = response.json()
    assert data['ip'] == digital_ocean_ip
    assert data['os_guess'] == "Linux/Unix"
    assert data['packet_size'] == 40
    assert data['ttl'] == 63


def test_banner_grab(api_base_url, auth_headers):
    """Test banner grabbing on a known port."""
    url = f"{api_base_url}/scan/bannergrab"
    response = requests.get(url, headers=auth_headers, params={"ip": "8.8.8.8", "port": 80})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
