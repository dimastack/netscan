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
