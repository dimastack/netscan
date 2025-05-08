import time

from scapy.all import IP, TCP, UDP, sr1, conf


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
