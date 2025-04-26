from flask import Blueprint, request, jsonify
from app.scanner import (
    ping_host, traceroute_host, syn_scan,
    udp_scan, banner_grab
)
import socket
from scapy.all import IP, TCP, sr1

scan_bp = Blueprint("scan", __name__)


@scan_bp.route("/ping")
def ping():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip'"}), 400
    return jsonify(ping_host(ip))


@scan_bp.route("/trace")
def trace():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip'"}), 400
    return jsonify(traceroute_host(ip))


@scan_bp.route("/synscan")
def synscan():
    ip = request.args.get("ip")
    ports = request.args.get("ports", "22,80,443")
    port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]
    return jsonify(syn_scan(ip, port_list))


@scan_bp.route("/tcpconnect")
def tcp_connect():
    ip = request.args.get("ip")
    port = request.args.get("port", type=int)

    if not ip or port is None:
        return jsonify({"error": "Missing 'ip' or 'port'"}), 400

    try:
        start = socket.time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        sock.close()
        end = socket.time.time()
        return jsonify({
            "ip": ip,
            "port": port,
            "status": "open",
            "rtt_ms": round((end - start) * 1000, 2)
        })
    except Exception as e:
        return jsonify({
            "ip": ip,
            "port": port,
            "status": "closed",
            "error": str(e)
        })


@scan_bp.route("/udp")
def udp():
    ip = request.args.get("ip")
    port = request.args.get("port", type=int)
    if not ip or port is None:
        return jsonify({"error": "Missing 'ip' or 'port'"}), 400
    return jsonify(udp_scan(ip, [port]))


@scan_bp.route("/portscan")
def portscan():
    ip = request.args.get("ip")
    port_range = request.args.get("range", "1-1024")

    try:
        start_port, end_port = map(int, port_range.split("-"))
    except Exception:
        return jsonify({"error": "Invalid port range format (use start-end)"}), 400

    ports = range(start_port, end_port + 1)
    return jsonify(syn_scan(ip, list(ports)))


@scan_bp.route("/osfingerprint")
def osfingerprint():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip'"}), 400

    pkt = IP(dst=ip)/TCP(dport=80, flags="S")
    resp = sr1(pkt, timeout=2, verbose=0)

    if not resp:
        return jsonify({"ip": ip, "status": "no response"})

    ttl = resp.ttl
    packet_size = len(resp)
    guess = "unknown"

    if ttl <= 64:
        guess = "Linux/Unix"
    elif ttl <= 128:
        guess = "Windows"
    elif ttl <= 255:
        guess = "Cisco/Network OS"

    return jsonify({
        "ip": ip,
        "ttl": ttl,
        "packet_size": packet_size,
        "os_guess": guess
    })


@scan_bp.route("/bannergrab")
def bannergrab():
    ip = request.args.get("ip")
    port = request.args.get("port", type=int)
    if not ip or port is None:
        return jsonify({"error": "Missing 'ip' or 'port'"}), 400
    return jsonify(banner_grab(ip, port))
