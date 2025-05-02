import requests
import ssl
import socket
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

web_bp = Blueprint("web", __name__)


@web_bp.route("/httpcheck")
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

    user_id = get_jwt_identity()

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


@web_bp.route("/sslcheck")
@jwt_required()
def ssl_check():
    """
    Inspect the SSL certificate for a given HTTPS URL.

    Query Parameters:
        url (str): The URL or domain to inspect.

    Returns:
        JSON object with issuer, subject, validity dates, and remaining days.
    """
    
    url = request.args.get("url")
    timeout = request.args.get("timeout", default=5, type=int)

    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    user_id = get_jwt_identity()

    try:
        parsed = urlparse(url if url.startswith("https") else "https://" + url)
        hostname = parsed.hostname
        port = parsed.port or 443

        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        return jsonify({
            "user_id": user_id,
            "hostname": hostname,
            "issuer": dict(x[0] for x in cert.get("issuer", [])),
            "subject": dict(x[0] for x in cert.get("subject", [])),
            "valid_from": cert.get("notBefore"),
            "valid_to": cert.get("notAfter"),
            "valid_days_remaining": _days_remaining(cert.get("notAfter")),
        })

    except Exception as e:
        return jsonify({"url": url, "error": str(e)}), 500


def _days_remaining(not_after_str):
    try:
        expiry = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
        return (expiry - datetime.utcnow()).days
    except Exception:
        return None
