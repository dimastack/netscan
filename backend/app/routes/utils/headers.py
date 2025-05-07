from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.net import get_http_headers
from app.db import db_session
from app.models import ScanResult

headers_bp = Blueprint("headers", __name__)


@headers_bp.route("/headers")
@jwt_required()
def headers():
    """
    Retrieve HTTP response headers from a specified URL.

    Query Parameters:
        url (str): The full URL to send the request to.

    Returns:
        JSON object with HTTP headers or an error message.
    """
    
    user_id = int(get_jwt_identity())
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    result = get_http_headers(url)

    with db_session() as session:
        session.add(ScanResult(
            user_id=user_id,
            scan_type="http_headers",
            target=url,
            result=str(result)
        ))

    return jsonify(result)
