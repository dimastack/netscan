import time
import sys
import re
import subprocess

from scapy.all import IP, ICMP, sr1


def ping_host(ip):
    """
    Ping a host using Scapy (Linux based env); fallback to system ping if Scapy fails (any OS).

    ICMP (ping), used by Scapy, requires raw sockets, which by default:
    - Root restricted in OSX and Windows (requires sudo/Admin rights + Npcap)
    - Are not allowed in unprivileged containers
    - Need CAP_NET_RAW Linux capability
    - Some host firewall or Docker bridge network settings may block or drop ICMP packets from containers

    Args:
        ip (str): IP address to ping.

    Returns:
        dict: Unified result with status, response time, reply_from, etc.
    """
    try:
        start = time.time()
        pkt = IP(dst=ip) / ICMP()
        reply = sr1(pkt, timeout=2, verbose=0)
        end = time.time()

        if reply:
            return {
                "ip": ip,
                "status": "up",
                "response_time_ms": round((end - start) * 1000, 2),
                "reply_from": reply.src,
                "ttl": reply.ttl,
                "packet_size": len(reply),
                "method": "scapy",
                "raw_output": None,
                "error": None
            }
    except Exception as e:
        return {
            "ip": ip,
            "status": "error",
            "response_time_ms": None,
            "reply_from": None,
            "ttl": None,
            "packet_size": None,
            "method": "scapy",
            "raw_output": None,
            "error": str(e)
        }

    return fallback_ping(ip)


def fallback_ping(ip):
    """
    Fallback ping using system command. Works on all platforms if ICMP is blocked.

    Args:
        ip (str): IP address to ping.

    Returns:
        dict: Unified ping response fields including TTL, packet size, and raw output.
    """
    try:
        if sys.platform.startswith("linux"):
            args = ["ping", "-c", "1", "-W", "1", ip]
        elif sys.platform == "darwin":
            args = ["ping", "-c", "1", "-t", "1", ip]
        elif sys.platform.startswith("win"):
            args = ["ping", "-n", "1", "-w", "1000", ip]
        else:
            raise RuntimeError(f"Unsupported platform: {sys.platform}")

        start = time.time()
        result = subprocess.run(args, capture_output=True, text=True, timeout=3)
        end = time.time()
        output = result.stdout.strip()
        error_output = result.stderr.strip()
        response_time = round((end - start) * 1000, 2)

        status = "up" if result.returncode == 0 else "down"
        ttl = None
        packet_size = None
        reply_from = ip if status == "up" else None

        ttl_match = re.search(r'ttl[=|:](\d+)', output, re.IGNORECASE)
        if ttl_match:
            ttl = int(ttl_match.group(1))

        size_match = re.search(r'(\d+)\s+bytes\s+from', output)
        if not size_match:
            size_match = re.search(r'bytes=(\d+)', output)  # Windows format
        if size_match:
            packet_size = int(size_match.group(1))

        ip_match = re.search(r'from\s+([\d\.]+)', output)
        if ip_match:
            reply_from = ip_match.group(1)

        return {
            "ip": ip,
            "status": status,
            "response_time_ms": response_time if status == "up" else None,
            "reply_from": reply_from,
            "ttl": ttl,
            "packet_size": packet_size,
            "method": "system_ping",
            "raw_output": output or error_output,
            "error": None if status == "up" else error_output
        }

    except Exception as e:
        return {
            "ip": ip,
            "status": "error",
            "response_time_ms": None,
            "reply_from": None,
            "ttl": None,
            "packet_size": None,
            "method": "system_ping",
            "raw_output": None,
            "error": str(e)
        }
