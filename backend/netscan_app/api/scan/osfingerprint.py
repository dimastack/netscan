from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from scapy.all import IP, TCP, sr1

from netscan_app.core.db import db_session
from netscan_app.models.scan_results import ScanResult

osfingerprint_bp = Blueprint("osfingerprint", __name__)

@osfingerprint_bp.route("/osfingerprint")
@jwt_required()
def osfingerprint():
    """
    Attempt to identify the operating system of a host using TCP/IP fingerprinting.

    Query Parameters:
        ip (str): IP address of the target host.
        ports (str, optional): Comma-separated list of ports to try (e.g., 80,443,22). Defaults to "22,80,443,8000,8080".
        timeout (int): Timeout for the connection in seconds. Default is 2 seconds.

    Returns:
        JSON with guessed OS, TTL, packet size, and port used.
    """
    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    ports_str = request.args.get("ports", default="22,80,443,8000,8080")
    timeout = float(request.args.get("timeout", default="2"))
    ports = [int(p.strip()) for p in ports_str.split(",") if p.strip().isdigit()]

    if not ip:
        return jsonify({"error": "Missing 'ip' parameter"}), 400

    response = None
    used_port = None

    for port in ports:
        pkt = IP(dst=ip) / TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=timeout, verbose=0)
        if resp:
            response = resp
            used_port = port
            break

    if not response:
        return jsonify({
            "ip": ip,
            "status": f"No response - tried ports {ports_str}. All failed or were filtered.",
        })

    ttl = response.ttl
    packet_size = len(response)
    guess = "unknown"

    if ttl <= 64:
        guess = "Linux/Unix"
    elif ttl <= 128:
        guess = "Windows"
    elif ttl <= 255:
        guess = "Cisco/Network OS"

    result = {
        "ip": ip,
        "port": used_port,
        "ttl": ttl,
        "packet_size": packet_size,
        "os_guess": guess
    }

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="osfingerprint",
            target=f"{ip}:{used_port}",
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)
