import socket


def banner_grab(ip, port, timeout=2):
    """
    Perform adaptive banner grabbing based on port behavior.

    Args:
        ip (str): Target IP address.
        port (int): Target port.
        timeout (int): Timeout in seconds.

    Returns:
        dict: Banner result with status and optional error.
    """

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))

        try:
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
        except socket.timeout:
            banner = ''

        # For HTTP-like ports, try sending GET request
        if not banner.strip() and port in [80, 8080, 8000]:
            request = f"GET / HTTP/1.1\r\nHost: {ip}\r\nConnection: close\r\n\r\n"
            sock.send(request.encode())
            banner = sock.recv(1024).decode('utf-8', errors='ignore')

        sock.close()

        return {
            "ip": ip,
            "port": port,
            "status": "open",
            "banner": banner.strip() or None
        }

    except Exception as e:
        return {
            "ip": ip,
            "port": port,
            "status": "closed",
            "banner": None,
            "error": str(e)
        }
