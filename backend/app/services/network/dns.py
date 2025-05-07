import socket


def resolve_hostname(hostname):
    """
    Resolve a hostname to an IP address.

    Args:
        hostname (str): The hostname to resolve.

    Returns:
        dict: A dictionary containing the hostname, IP address, and any error encountered.
    """

    try:
        ip = socket.gethostbyname(hostname)
        return {
            "hostname": hostname, 
            "ip": ip,
            "error": None
        }
    except Exception as e:
        return {
            "hostname": hostname, 
            "ip": None,
            "error": str(e)
        }


def reverse_dns(ip):
    """
    Perform a reverse DNS lookup to get the hostname from an IP address.

    Args:
        ip (str): The IP address to resolve.

    Returns:
        dict: A dictionary containing the IP address, hostname, and any error encountered.
    """
    
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return {
            "ip": ip, 
            "hostname": hostname,
            "error": None
        }
    except Exception as e:
        return {
            "ip": ip, 
            "hostname": None,
            "error": str(e)
        }
