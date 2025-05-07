import socket
import time
import sys
import re
import subprocess
from scapy.all import IP, ICMP, TCP, UDP, sr1, conf


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

        # Parse TTL
        ttl_match = re.search(r'ttl[=|:](\d+)', output, re.IGNORECASE)
        if ttl_match:
            ttl = int(ttl_match.group(1))

        # Parse packet size
        size_match = re.search(r'(\d+)\s+bytes\s+from', output)
        if not size_match:
            size_match = re.search(r'bytes=(\d+)', output)  # Windows format
        if size_match:
            packet_size = int(size_match.group(1))

        # Optionally parse real reply IP
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

def traceroute_host(ip, max_hops=30):
    """
    Traceroute a host using Scapy or fallback to system traceroute 
    if Scapy fails because of ICMP and blocked sockets.

    Wasn't able to make traceroute testable in Docker on OSX (even as ping works),
    because Docker on OSX is running inside lightweight Linux VM and 
    the container’s network traffic is NAT-ed through this VM. 
    ICMP and certain UDP packets used by traceroute do not traverse this NAT cleanly and
    that's why traffic can't pass the first gateway inside the VM.

    !! NOTE: I was able to find 'mtr-tiny' tool, which on OSX shows 
    2 hops (container gateway and final result via ping).
    But I don't want to add mtr-tiny to support better 
    fallback results for Docker on OSX\Windows on current moment.

    Args:
        ip (str): The target IP address.
        max_hops (int): The maximum number of hops (TTL values) to trace.

    Returns:
        dict: The unified traceroute response.
    """
    try:
        # Scapy-based traceroute
        hops = []
        for ttl in range(1, max_hops + 1):
            pkt = IP(dst=ip, ttl=ttl)/ICMP()
            start = time.time()
            reply = sr1(pkt, timeout=2, verbose=0)
            end = time.time()

            hop_data = {
                "ttl": ttl,
                "rtt_ms": round((end - start) * 1000, 2)
            }

            if reply:
                hop_data["ip"] = reply.src
                hop_data["status"] = "ok"
            else:
                hop_data["ip"] = None
                hop_data["status"] = "timeout"

            hops.append(hop_data)
            
            # If the reply's source matches the destination IP, stop early
            if reply and reply.src == ip:
                break

        return {
            "ip": ip,
            "method": "scapy",
            "hops": hops,
            "raw_output": None,
            "error": None        
        }
    
    except Exception as scapy_error:
        # If Scapy fails, fallback to system-based traceroute
        try:
            if sys.platform.startswith("linux"):
                args = ["traceroute", ip]
            elif sys.platform == "darwin":
                args = ["traceroute", ip]
            elif sys.platform.startswith("win"):
                args = ["tracert", ip]
            else:
                raise RuntimeError(f"Unsupported platform: {sys.platform}")

            # Execute traceroute command
            result = subprocess.run(args, capture_output=True, text=True, timeout=15)
            hops = parse_traceroute_output(result.stdout)

            return {
                "ip": ip,
                "method": "system_traceroute",  # Indicating the fallback method
                "hops": hops,
                "raw_output": result.stdout.strip() if result.stdout else result.stderr.strip(),
                "error": None
            }

        except Exception as e:
            return {
                "ip": ip,
                "method": "system_traceroute",
                "hops": [],
                "raw_output": None,
                "error": str(e)
            }

def parse_traceroute_output(output):
    """
    Helper function to parse the raw traceroute output into a unified format.

    Args:
        output (str): Raw output from the system traceroute command.

    Returns:
        list: List of hops with TTL, IP, status, and RTT.
    """
    hops = []
    lines = output.splitlines()

    for line in lines:
        if sys.platform.startswith("linux") or sys.platform == "darwin":
            # Example: "1  192.168.1.1 (192.168.1.1)  0.457 ms  0.336 ms  0.319 ms"
            parts = line.split()
            if len(parts) >= 2:
                ttl = int(parts[0])
                ip = parts[1].strip("()")
                rtt = parts[2] if len(parts) > 2 else None
                hops.append({
                    "ttl": ttl,
                    "ip": ip,
                    "status": "ok",
                    "rtt_ms": rtt if rtt else None
                })
        elif sys.platform.startswith("win"):
            parts = line.split()
            if len(parts) >= 2:
                ttl = int(parts[0])
                ip = parts[3]
                rtt = parts[1] if len(parts) > 1 else None
                hops.append({
                    "ttl": ttl,
                    "ip": ip,
                    "status": "ok",
                    "rtt_ms": rtt if rtt else None
                })

    return hops

def syn_scan(ip, ports):
    """
    Perform a TCP SYN scan on the specified IP address and list of ports.

    Args:
        ip (str): The target IP address.
        ports (list[int]): A list of TCP ports to scan.

    Returns:
        dict: A dictionary containing the target IP and a list of results.
              Each result includes port number, round-trip time (rtt_ms),
              scan status (open, closed, filtered, etc.), response flags,
              and the IP address that replied.
    """

    conf.verb = 0
    results = []

    for port in ports:
        pkt = IP(dst=ip)/TCP(dport=port, flags="S")
        start = time.time()
        resp = sr1(pkt, timeout=2, verbose=0)
        end = time.time()

        rtt = round((end - start) * 1000, 2)
        result = {
            "port": port,
            "rtt_ms": rtt
        }

        if resp is None:
            result["status"] = "filtered"
            result["flags"] = None
            result["reply_from"] = None
        elif resp.haslayer(TCP):
            tcp_flags = resp.getlayer(TCP).flags
            result["reply_from"] = resp.src
            result["flags"] = str(tcp_flags)
            if tcp_flags == 0x12:
                result["status"] = "open"
            elif tcp_flags == 0x14:
                result["status"] = "closed"
            else:
                result["status"] = "unknown"
        else:
            result["status"] = "non-tcp-response"
            result["flags"] = None
            result["reply_from"] = resp.src if resp else None

        results.append(result)

    return {
        "ip": ip,
        "results": results
    }


def udp_scan(ip, ports):
    """
    Perform a UDP scan on the specified IP address and list of ports.

    Args:
        ip (str): The target IP address.
        ports (list[int]): A list of UDP ports to scan.

    Returns:
        dict: A dictionary containing the target IP and a list of results.
              Each result includes port number, round-trip time (rtt_ms),
              scan status ("open|filtered" or "closed"), and the IP address
              that replied (if any).
    """

    conf.verb = 0
    results = []

    for port in ports:
        pkt = IP(dst=ip)/UDP(dport=port)
        start = time.time()
        resp = sr1(pkt, timeout=2, verbose=0)
        end = time.time()

        rtt = round((end - start) * 1000, 2)
        result = {
            "port": port,
            "rtt_ms": rtt
        }

        if resp is None:
            result["status"] = "open|filtered"
            result["reply_from"] = None
        else:
            result["status"] = "closed"
            result["reply_from"] = resp.src

        results.append(result)

    return {
        "ip": ip,
        "results": results
    }


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
