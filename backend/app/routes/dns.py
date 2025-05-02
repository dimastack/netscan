import whois
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from scapy.all import IP, UDP, DNS, DNSQR, sr1

from app.db import db_session
from app.models.scan_result import ScanResult

dns_bp = Blueprint("dns", __name__)

@dns_bp.route("/lookup")
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

    # Get user_id from JWT token
    user_id = get_jwt_identity()

    domain = request.args.get("domain")
    record_type = request.args.get("type", default="A").upper()
    dst = request.args.get("dst", default="8.8.8.8")
    timeout = float(request.args.get("timeout", default="2"))

    supported_types = {"A", "AAAA", "MX", "CNAME", "TXT"}
    if not domain:
        return jsonify({"error": "Missing 'domain' parameter"}), 400
    if record_type not in supported_types:
        return jsonify({"error": f"Unsupported record type '{record_type}'"}), 400

    try:
        pkt = IP(dst=dst) / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype=record_type))
        resp = sr1(pkt, verbose=0, timeout=timeout)

        results = []
        if resp and resp.haslayer(DNS):
            for i in range(resp[DNS].ancount):
                r = resp[DNS].an[i]
                try:
                    data = r.rdata.decode() if hasattr(r.rdata, "decode") else str(r.rdata)
                    results.append(data)
                except Exception:
                    results.append(str(r.rdata))

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

    except Exception as e:
        return jsonify({"domain": domain, "type": record_type, "error": str(e)}), 500


@dns_bp.route("/reverse")
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
    
    user_id = get_jwt_identity()

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


@dns_bp.route("/whois")
@jwt_required()
def whois_lookup():
    """
    Perform a WHOIS lookup for a domain.

    Query Parameters:
        domain (str): The domain name to look up WHOIS information for.

    Returns:
        JSON with WHOIS data such as registrar, creation/expiration dates, name servers, and contact email.
    """

    user_id = get_jwt_identity()

    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Missing 'domain' parameter"}), 400

    try:
        w = whois.whois(domain)
        result_data = {
            "domain": domain,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "emails": w.emails
        }

        with db_session() as session:
            result = ScanResult(
                user_id=user_id,
                scan_type="whois",
                target=domain,
                result=str(result_data)
            )
            session.add(result)

        return jsonify(result_data)

    except Exception as e:
        return jsonify({"domain": domain, "error": str(e)}), 500
