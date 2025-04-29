import socket
import time
from scapy.all import IP, ICMP, TCP, UDP, sr1, conf


def ping_host(ip):
    start = time.time()
    pkt = IP(dst=ip)/ICMP()
    reply = sr1(pkt, timeout=2, verbose=0)
    end = time.time()

    if reply:
        return {
            "ip": ip,
            "status": "up",
            "response_time_ms": round((end - start) * 1000, 2),
            "reply_from": reply.src,
            "ttl": reply.ttl,
            "packet_size": len(reply)
        }
    else:
        return {
            "ip": ip,
            "status": "down",
            "response_time_ms": None,
            "reply_from": None,
            "ttl": None,
            "packet_size": None
        }


def traceroute_host(ip, max_hops=30):
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
        "hops": hops
    }


def syn_scan(ip, ports):
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
