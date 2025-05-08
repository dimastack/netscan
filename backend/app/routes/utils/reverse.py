import socket

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.core.db import db_session
from app.models import ScanResult

reverse_bp = Blueprint("reverse", __name__)


@reverse_bp.route("/reverse")
@jwt_required()
def reverse():
    """
    Perform reverse DNS lookup on an IP address.

    Query Parameters:
        ip (str): The IP address to reverse-resolve.

    Returns:
        JSON response with the hostname or error message.
    """

    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip' parameter"}), 400

    try:
        hostname = socket.gethostbyaddr(ip)[0]
        result = {
            "ip": ip, 
            "hostname": hostname,
            "error": None
        }
    except Exception as e:
        result = {
            "ip": ip, 
            "hostname": None,
            "error": str(e)
        }

    with db_session() as session:
        session.add(ScanResult(
            user_id=user_id,
            scan_type="reverse_dns",
            target=ip,
            result=str(result)
        ))

    return jsonify(result)
