from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.net import resolve_hostname
from app.db import db_session
from app.models import ScanResult

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

    result = resolve_hostname(host)

    with db_session() as session:
        session.add(ScanResult(
            user_id=user_id,
            scan_type="resolve",
            target=host,
            result=str(result)
        ))

    return jsonify(result)
