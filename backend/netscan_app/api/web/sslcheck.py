import ssl
import socket

from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

sslcheck_bp = Blueprint("sslcheck", __name__)


@sslcheck_bp.route("/sslcheck")
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

    user_id = int(get_jwt_identity())

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
