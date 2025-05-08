import socket


def banner_grab(ip, port):
    """
    Perform a basic banner grabbing operation on the specified IP and port.

    Args:
        ip (str): The target IP address.
        port (int): The target port number.

    Returns:
        dict: A dictionary containing the IP, port, connection status ("open" or "closed"),
              the retrieved banner (if any), and error message (if applicable).
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        sock.send(b'GET / HTTP/1.1\r\nHost: %s\r\n\r\n' % ip.encode())
        banner = sock.recv(1024).decode('utf-8', errors='ignore')
        sock.close()
        return {
            "ip": ip,
            "port": port,
            "status": "open",
            "banner": banner.strip()
        }
    except Exception as e:
        return {
            "ip": ip,
            "port": port,
            "status": "closed",
            "banner": None,
            "error": str(e)
        }
