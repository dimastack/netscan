from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.network import check_latency
from app.core.db import db_session
from app.models import ScanResult

latency_bp = Blueprint("latency", __name__)


@latency_bp.route("/latency")
@jwt_required()
def latency():
    """
    Measure TCP latency to a specified host and port.

    Query Parameters:
        host (str): Target host or IP.
        port (int): Target port (default: 80).

    Returns:
        JSON with round-trip time in milliseconds, or an error.
    """

    user_id = int(get_jwt_identity())
    host = request.args.get("host")
    port = request.args.get("port", default=80, type=int)
    if not host:
        return jsonify({"error": "Missing 'host' parameter"}), 400

    result = check_latency(host, port)

    with db_session() as session:
        session.add(ScanResult(
            user_id=user_id,
            scan_type="latency",
            target=f"{host}:{port}",
            result=str(result)
        ))

    return jsonify(result)
