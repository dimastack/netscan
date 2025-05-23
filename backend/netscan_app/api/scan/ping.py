from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from netscan_app.core.db import db_session
from netscan_app.models.scan_results import ScanResult
from netscan_app.services.scanner import ping_host

ping_bp = Blueprint("ping", __name__)

@ping_bp.route("/ping")
@jwt_required()
def ping():
    """
    Ping a host to check if it's reachable.

    Query Parameters:
        ip (str): IP address of the host to ping.
        timeout (int): Timeout for the connection in seconds. Default is 3 seconds.

    Returns:
        JSON with ICMP ping result.
    """

    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    timeout = float(request.args.get("timeout", default="3"))
    if not ip:
        return jsonify({"error": "Missing 'ip'"}), 400

    result = ping_host(ip, timeout)

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="ping",
            target=ip,
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)
