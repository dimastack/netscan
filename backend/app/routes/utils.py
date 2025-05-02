from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.utils.net import resolve_hostname, reverse_dns, check_latency, get_http_headers
from app.db import db_session
from app.models import ScanResult

utils_bp = Blueprint("utils", __name__)


@utils_bp.route("/resolve")
@jwt_required()
def resolve():
    """
    Resolve hostname to IP addresses.

    Query Parameters:
        host (str): The domain name or hostname to resolve.

    Returns:
        JSON response with resolved IP addresses or an error message.
    """

    user_id = get_jwt_identity()
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


@utils_bp.route("/reverse")
@jwt_required()
def reverse():
    """
    Perform reverse DNS lookup on an IP address.

    Query Parameters:
        ip (str): The IP address to reverse-resolve.

    Returns:
        JSON response with the hostname or error message.
    """

    user_id = get_jwt_identity()
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip' parameter"}), 400

    result = reverse_dns(ip)

    with db_session() as session:
        session.add(ScanResult(
            user_id=user_id,
            scan_type="reverse_dns",
            target=ip,
            result=str(result)
        ))

    return jsonify(result)


@utils_bp.route("/latency")
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

    user_id = get_jwt_identity()
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


@utils_bp.route("/headers")
@jwt_required()
def headers():
    """
    Retrieve HTTP response headers from a specified URL.

    Query Parameters:
        url (str): The full URL to send the request to.

    Returns:
        JSON object with HTTP headers or an error message.
    """
    
    user_id = get_jwt_identity()
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
