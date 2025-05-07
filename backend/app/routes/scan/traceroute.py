from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.db import db_session
from app.models.scan_results import ScanResult
from app.scanner import traceroute_host

traceroute_bp = Blueprint("trace", __name__, url_prefix="/scan")

@traceroute_bp.route("/trace")
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
