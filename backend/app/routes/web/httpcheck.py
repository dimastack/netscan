import requests

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

httpcheck_bp = Blueprint("httpcheck", __name__, url_prefix="/web")


@httpcheck_bp.route("/httpcheck")
@jwt_required()
def http_check():
    """
    Perform an HTTP GET request to a given URL and return detailed response metadata.

    Query Parameters:
        url (str): The URL to check.

    Returns:
        JSON object containing status code, headers, redirects, HSTS presence, and more.
    """

    url = request.args.get("url")
    timeout = request.args.get("timeout", default=5, type=int)

    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    user_id = int(get_jwt_identity())

    try:
        response = requests.get(url, timeout=timeout, allow_redirects=True)
        return jsonify({
            "user_id": user_id,
            "url": response.url,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "redirects": [resp.url for resp in response.history],
            "hsts": "strict-transport-security" in response.headers,
            "content_type": response.headers.get("Content-Type"),
            "length": len(response.content)
        })
    except Exception as e:
        return jsonify({"url": url, "error": str(e)}), 500
