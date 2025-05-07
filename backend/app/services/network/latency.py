import socket
import time


def check_latency(host, port=80, timeout=2):
    """
    Check the latency of a connection to a given host and port.

    Args:
        host (str): The host to check.
        port (int): The port to check the latency for (default is 80).
        timeout (int): The connection timeout in seconds (default is 2 seconds).

    Returns:
        dict: A dictionary containing the host, port, connection status, latency, and any error encountered.
    """
    
    try:
        start = time.time()
        sock = socket.create_connection((host, port), timeout=timeout)
        end = time.time()
        sock.close()
        return {
            "host": host,
            "port": port,
            "status": "online",
            "latency_ms": round((end - start) * 1000, 2),
            "error": None
        }
    except Exception as e:
        return {
            "host": host,
            "port": port,
            "status": "offline",
            "latency_ms": None,
            "error": str(e)
        }
