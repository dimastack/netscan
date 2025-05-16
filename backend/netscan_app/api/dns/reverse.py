from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from scapy.all import IP, UDP, DNS, DNSQR, sr1
import dns.resolver
import dns.reversename

from netscan_app.core.db import db_session
from netscan_app.models.scan_results import ScanResult

reverse_bp = Blueprint("reverse", __name__)

@reverse_bp.route("/reverse")
@jwt_required()
def reverse():
    """
    Perform a reverse DNS lookup for a given IP address, using Scapy first,
    and falling back to dnspython if necessary.
    """
    user_id = int(get_jwt_identity())

    ip = request.args.get("ip")
    dst = request.args.get("dst", default="8.8.8.8")
    timeout = float(request.args.get("timeout", default="2"))

    if not ip:
        return jsonify({"error": "Missing 'ip' parameter"}), 400

    hostname = None

    try:
        reversed_ip = '.'.join(reversed(ip.split('.'))) + '.in-addr.arpa'
        pkt = IP(dst=dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=reversed_ip, qtype="PTR"))
        resp = sr1(pkt, verbose=0, timeout=timeout)

        if resp and resp.haslayer(DNS) and resp[DNS].ancount > 0:
            hostname = resp[DNS].an.rdata.decode()
    except Exception as e:
        pass

    if not hostname:
        try:
            rev_name = dns.reversename.from_address(ip)
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dst]
            answer = resolver.resolve(rev_name, "PTR", lifetime=timeout)
            hostname = str(answer[0])
        except Exception:
            hostname = None

    # Save result to DB
    with db_session() as session:
        result_data = ScanResult(
            user_id=user_id,
            scan_type="dns_reverse",
            target=ip,
            result=hostname or "not found"
        )
        session.add(result_data)

    if hostname:
        return jsonify({"ip": ip, "hostname": hostname})
    else:
        return jsonify({"ip": ip, "hostname": None, "status": "not found"})
