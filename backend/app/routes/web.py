import requests
import ssl
import socket
from flask import Blueprint, request, jsonify
from urllib.parse import urlparse
from datetime import datetime

web_bp = Blueprint("web", __name__)


@web_bp.route("/httpcheck")
def http_check():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        return jsonify({
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
def ssl_check():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        parsed = urlparse(url if url.startswith("https") else "https://" + url)
        hostname = parsed.hostname
        port = parsed.port or 443

        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        return jsonify({
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
