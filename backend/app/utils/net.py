import socket
import time
import requests


def resolve_hostname(hostname):
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


def check_latency(host, port=80, timeout=2):
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


def get_http_headers(url):
    try:
        resp = requests.head(url, timeout=3)
        return {
            "url": url,
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "error": None
        }
    except Exception as e:
        return {
            "url": url,
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "error": str(e)
        }
