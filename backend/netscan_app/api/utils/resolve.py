import socket

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from netscan_app.core.db import db_session
from netscan_app.models import ScanResult

resolve_bp = Blueprint("resolve", __name__)


@resolve_bp.route("/resolve")
@jwt_required()
def resolve():
    """
    Resolve hostname to IP addresses.

    Query Parameters:
        host (str): The domain name or hostname to resolve.

    Returns:
        JSON response with resolved IP addresses or an error message.
    """

    user_id = int(get_jwt_identity())
    host = request.args.get("host")
    if not host:
        return jsonify({"error": "Missing 'host' parameter"}), 400

    try:
        ip = socket.gethostbyname(host)
        result = {
            "hostname": host, 
            "ip": ip,
            "error": None
        }
    except Exception as e:
        result = {
            "hostname": host, 
            "ip": None,
            "error": str(e)
        }

    with db_session() as session:
        session.add(ScanResult(
            user_id=user_id,
            scan_type="resolve",
            target=host,
            result=str(result)
        ))

    return jsonify(result)
