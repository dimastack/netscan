from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from netscan_app.core.db import db_session
from netscan_app.models.scan_results import ScanResult
from netscan_app.services.scanner import banner_grab

banner_bp = Blueprint("banner", __name__)


@banner_bp.route("/bannergrab")
@jwt_required()
def bannergrab():
    """
    Grab a service banner from a TCP port.

    Query Parameters:
        ip (str): IP address of the target host.
        port (int): Port number to connect to.
        timeout (int): Timeout for the connection in seconds. Default is 2 seconds.

    Returns:
        JSON with banner string or error details.
    """
    
    user_id = int(get_jwt_identity())
    ip = request.args.get("ip")
    port = request.args.get("port", type=int)
    timeout = float(request.args.get("timeout", default="2"))
    if not ip or port is None:
        return jsonify({"error": "Missing 'ip' or 'port'"}), 400

    result = banner_grab(ip, port, timeout=timeout)

    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="bannergrab",
            target=f"{ip}:{port}",
            result=str(result)
        )
        session.add(result_data)

    return jsonify(result)
