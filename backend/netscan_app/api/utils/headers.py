import requests

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from netscan_app.core.db import db_session
from netscan_app.models import ScanResult

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

    try:
        resp = requests.head(url, timeout=3)
        result = {
            "url": url,
            "status_code": resp.status_code,
            "headers": dict(resp.headers),
            "error": None
        }
    except Exception as e:
        result = {
            "url": url,
            "status_code": None,
            "headers": None,
            "error": str(e)
        }

    with db_session() as session:
        session.add(ScanResult(
            user_id=user_id,
            scan_type="http_headers",
            target=url,
            result=str(result)
        ))

    return jsonify(result)
