from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from scapy.all import IP, UDP, DNS, DNSQR, sr1
import dns.resolver

from netscan_app.core.db import db_session
from netscan_app.models.scan_results import ScanResult

lookup_bp = Blueprint("lookup", __name__)

@lookup_bp.route("/lookup")
@jwt_required()
def lookup():
    """
    Perform a DNS lookup for the specified domain and record type.

    Query Parameters:
        domain (str): The domain name to query (e.g., example.com).
        type (str, optional): DNS record type (e.g., A, AAAA, MX, CNAME, TXT). Defaults to 'A'.
        dst (str, optional): DNS server to query. Defaults to '8.8.8.8'.
        timeout (int, optional): Timeout for the query in seconds. Defaults to 2.

    Returns:
        JSON with the DNS response answers or an error message.
    """

    user_id = int(get_jwt_identity())

    domain = request.args.get("domain")
    record_type = request.args.get("type", default="A").upper()
    dst = request.args.get("dst", default="8.8.8.8")
    timeout = float(request.args.get("timeout", default="2"))

    supported_types = {"A", "AAAA", "MX", "CNAME", "TXT"}
    if not domain:
        return jsonify({"error": "Missing 'domain' parameter"}), 400
    if record_type not in supported_types:
        return jsonify({"error": f"Unsupported record type '{record_type}'"}), 400

    results = []

    try:
        pkt = IP(dst=dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype=record_type))
        resp = sr1(pkt, verbose=0, timeout=timeout)

        if resp and resp.haslayer(DNS):
            for i in range(resp[DNS].ancount):
                r = resp[DNS].an[i]
                try:
                    data = r.rdata.decode() if hasattr(r.rdata, "decode") else str(r.rdata)
                    results.append(data)
                except Exception:
                    results.append(str(r.rdata))
    except Exception:
        pass

    if not results:
        try:
            resolver = dns.resolver.Resolver()
            resolver.nameservers = [dst]
            answer = resolver.resolve(domain, record_type, lifetime=timeout)
            results = [str(r) for r in answer]
        except Exception as e:
            if "The DNS response does not contain an answer to the question" in str(e):
                return jsonify({
                    "domain": domain,
                    "type": record_type,
                    "answers": [f"{str(e)}"]
                }), 200
            else:
                return jsonify({
                    "domain": domain,
                    "type": record_type,
                    "error": f"DNS query error: {str(e)}"
                }), 500

    with db_session() as session:
        result = ScanResult(
            user_id=user_id,
            scan_type="dns_lookup",
            target=domain,
            result=str(results)
        )
        session.add(result)

    return jsonify({
        "domain": domain,
        "type": record_type,
        "answers": results
    })
