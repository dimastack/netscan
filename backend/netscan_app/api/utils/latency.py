import socket
import time

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from netscan_app.core.db import db_session
from netscan_app.models import ScanResult

latency_bp = Blueprint("latency", __name__)


@latency_bp.route("/latency")
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

    user_id = int(get_jwt_identity())
    host = request.args.get("host")
    port = request.args.get("port", default=80, type=int)
    if not host:
        return jsonify({"error": "Missing 'host' parameter"}), 400

    try:
        start = time.time()
        sock = socket.create_connection((host, port), timeout=2)
        end = time.time()
        sock.close()
        result = {
            "host": host,
            "port": port,
            "status": "online",
            "latency_ms": round((end - start) * 1000, 2),
            "error": None
        }
    except Exception as e:
        result = {
            "host": host,
            "port": port,
            "status": "offline",
            "latency_ms": None,
            "error": str(e)
        }

    with db_session() as session:
        session.add(ScanResult(
            user_id=user_id,
            scan_type="latency",
            target=f"{host}:{port}",
            result=str(result)
        ))

    return jsonify(result)
