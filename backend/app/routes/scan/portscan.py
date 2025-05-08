import socket
import time

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.core.db import db_session
from app.models.scan_results import ScanResult
from app.services.scanner import syn_scan, udp_scan

portscan_bp = Blueprint("portscan", __name__)

@portscan_bp.route("/synscan")
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


@portscan_bp.route("/tcpconnect")
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
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        sock.close()
        end = time.time()

        result = {
            "ip": ip,
            "port": port,
            "status": "open",
            "rtt_ms": round((end - start) * 1000, 2),
            "error": None
        }
    except Exception as e:
        result = {
            "ip": ip,
            "port": port,
            "status": "closed",
            "error": str(e),
            "rtt_ms": None
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


@portscan_bp.route("/udp")
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


@portscan_bp.route("/portscan")
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
