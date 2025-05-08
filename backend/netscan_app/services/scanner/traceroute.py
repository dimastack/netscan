import time
import sys
import subprocess

from scapy.all import IP, ICMP, sr1


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

            if reply and reply.src == ip:
                break

        return {
            "ip": ip,
            "method": "scapy",
            "hops": hops,
            "raw_output": None,
            "error": None        
        }

    except Exception:
        return system_traceroute(ip)


def system_traceroute(ip):
    try:
        if sys.platform.startswith("linux") or sys.platform == "darwin":
            args = ["traceroute", ip]
        elif sys.platform.startswith("win"):
            args = ["tracert", ip]
        else:
            raise RuntimeError(f"Unsupported platform: {sys.platform}")

        result = subprocess.run(args, capture_output=True, text=True, timeout=15)
        hops = parse_traceroute_output(result.stdout)

        return {
            "ip": ip,
            "method": "system_traceroute",
            "hops": hops,
            "raw_output": result.stdout.strip() or result.stderr.strip(),
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
        parts = line.split()
        if sys.platform.startswith("linux") or sys.platform == "darwin":
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
