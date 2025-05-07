import socket
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from scapy.all import IP, TCP, sr1

from app.db import db_session
from app.models.scan_result import ScanResult
from app.scanner import (
    ping_host, traceroute_host, syn_scan,
    udp_scan, banner_grab
)

scan_bp = Blueprint("scan", __name__, url_prefix="/scan")

@scan_bp.route("/ping")
@jwt_required()
def ping():
    """
    Ping a host to check if it's reachable.

    Query Parameters:
        ip (str): IP address of the host to ping.

    Returns:
        JSON with ICMP ping result.
    """

    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip'"}), 400

    result = ping_host(ip)

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="ping",
            target=ip,
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)


@scan_bp.route("/trace")
@jwt_required()
def trace():
    """
    Perform a traceroute to a given IP address.

    Query Parameters:
        ip (str): IP address to trace the route to.

    Returns:
        JSON with list of hops to the destination.
    """

    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip'"}), 400

    result = traceroute_host(ip)

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="trace",
            target=ip,
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)


@scan_bp.route("/synscan")
@jwt_required()
def synscan():
    """
    Perform a TCP SYN port scan on a host.

    Query Parameters:
        ip (str): IP address of the target host.
        ports (str): Comma-separated list of ports (e.g., 22,80,443).

    Returns:
        JSON with scan results showing open ports.
    """

    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    ports = request.args.get("ports", "22,80,443")
    port_list = [int(p.strip()) for p in ports.split(",") if p.strip().isdigit()]

    result = syn_scan(ip, port_list)

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="synscan",
            target=ip,
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)


@scan_bp.route("/tcpconnect")
@jwt_required()
def tcp_connect():
    """
    Attempt to establish a TCP connection to check if a port is open.

    Query Parameters:
        ip (str): IP address of the target host.
        port (int): Port number to test.

    Returns:
        JSON with connection status and response time (RTT).
    """

    user_id = int(get_jwt_identity())
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

        result = {
            "ip": ip,
            "port": port,
            "status": "open",
            "rtt_ms": round((end - start) * 1000, 2)
        }

        with db_session() as session:
            result_data = ScanResult(
                user_id=user_id,
                scan_type="tcpconnect",
                target=f"{ip}:{port}",
                result=str(result)
            )
            session.add(result_data)

        return jsonify(result)

    except Exception as e:
        result = {
            "ip": ip,
            "port": port,
            "status": "closed",
            "error": str(e)
        }
        with db_session() as session:
            result_data = ScanResult(
                user_id=user_id,
                scan_type="tcpconnect",
                target=f"{ip}:{port}",
                result=str(result)
            )
            session.add(result_data)

        return jsonify(result)


@scan_bp.route("/udp")
@jwt_required()
def udp():
    """
    Perform a UDP port scan on a specific port.

    Query Parameters:
        ip (str): IP address of the target host.
        port (int): Port number to test.

    Returns:
        JSON with scan result for the given UDP port.
    """

    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    port = request.args.get("port", type=int)
    if not ip or port is None:
        return jsonify({"error": "Missing 'ip' or 'port'"}), 400

    result = udp_scan(ip, [port])

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="udp",
            target=f"{ip}:{port}",
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)


@scan_bp.route("/portscan")
@jwt_required()
def portscan():
    """
    Perform a port range scan using TCP SYN.

    Query Parameters:
        ip (str): IP address of the target host.
        range (str): Port range in 'start-end' format (e.g., 20-80).

    Returns:
        JSON with scan results showing open ports within the range.
    """

    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    port_range = request.args.get("range", "1-1024")

    try:
        start_port, end_port = map(int, port_range.split("-"))
    except Exception:
        return jsonify({"error": "Invalid port range format (use start-end)"}), 400

    ports = range(start_port, end_port + 1)
    result = syn_scan(ip, list(ports))

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="portscan",
            target=ip,
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)


@scan_bp.route("/osfingerprint")
@jwt_required()
def osfingerprint():
    """
    Attempt to identify the operating system of a host.

    Query Parameters:
        ip (str): IP address of the target host.

    Returns:
        JSON with guessed OS, TTL, and packet size.
    """

    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip'"}), 400

    pkt = IP(dst=ip) / TCP(dport=80, flags="S")
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

    result = {
        "ip": ip,
        "ttl": ttl,
        "packet_size": packet_size,
        "os_guess": guess
    }

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="osfingerprint",
            target=ip,
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)


@scan_bp.route("/bannergrab")
@jwt_required()
def bannergrab():
    """
    Grab a service banner from a TCP port.

    Query Parameters:
        ip (str): IP address of the target host.
        port (int): Port number to connect to.

    Returns:
        JSON with banner string or error details.
    """
    
    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    port = request.args.get("port", type=int)
    if not ip or port is None:
        return jsonify({"error": "Missing 'ip' or 'port'"}), 400

    result = banner_grab(ip, port)

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="bannergrab",
            target=f"{ip}:{port}",
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)
