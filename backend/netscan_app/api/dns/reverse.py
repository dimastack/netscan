from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from scapy.all import IP, UDP, DNS, DNSQR, sr1

from netscan_app.core.db import db_session
from netscan_app.models.scan_results import ScanResult

reverse_bp = Blueprint("reverse", __name__)


@reverse_bp.route("/reverse")
@jwt_required()
def reverse():
    """
    Perform a reverse DNS lookup for a given IP address.

    Query Parameters:
        ip (str): The IP address to reverse-lookup (e.g., 8.8.8.8).
        dst (str, optional): DNS server to query. Defaults to '8.8.8.8'.
        timeout (int, optional): Timeout for the query in seconds. Defaults to 2.

    Returns:
        JSON with the resolved hostname or 'not found' if unavailable.
    """
    
    user_id = int(get_jwt_identity())

    ip = request.args.get("ip")
    dst = request.args.get("dst", default="8.8.8.8")
    timeout = float(request.args.get("timeout", default="2"))

    if not ip:
        return jsonify({"error": "Missing 'ip' parameter"}), 400

    try:
        reversed_ip = '.'.join(reversed(ip.split('.'))) + '.in-addr.arpa'
        pkt = IP(dst=dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=reversed_ip, qtype="PTR"))
        resp = sr1(pkt, verbose=0, timeout=timeout)

        if resp and resp.haslayer(DNS) and resp[DNS].ancount > 0:
            ptr_record = resp[DNS].an.rdata.decode()

            with db_session() as session:
                result = ScanResult(
                    user_id=user_id,
                    scan_type="dns_reverse",
                    target=ip,
                    result=ptr_record
                )
                session.add(result)
            return jsonify({"ip": ip, "hostname": ptr_record})
        else:
            return jsonify({"ip": ip, "hostname": None, "status": "not found"})

    except Exception as e:
        return jsonify({"ip": ip, "error": str(e)}), 500
