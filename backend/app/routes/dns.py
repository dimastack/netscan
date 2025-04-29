from flask import Blueprint, request, jsonify
from scapy.all import IP, UDP, DNS, DNSQR, sr1
import whois

dns_bp = Blueprint("dns", __name__)


@dns_bp.route("/lookup")
def lookup():
    domain = request.args.get("domain")
    record_type = request.args.get("type", default="A").upper()

    supported_types = {"A", "AAAA", "MX", "CNAME", "TXT"}
    if not domain:
        return jsonify({"error": "Missing 'domain' parameter"}), 400
    if record_type not in supported_types:
        return jsonify({"error": f"Unsupported record type '{record_type}'"}), 400

    try:
        pkt = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=domain, qtype=record_type))
        resp = sr1(pkt, verbose=0, timeout=2)

        results = []
        if resp and resp.haslayer(DNS):
            for i in range(resp[DNS].ancount):
                r = resp[DNS].an[i]
                try:
                    data = r.rdata.decode() if hasattr(r.rdata, "decode") else str(r.rdata)
                    results.append(data)
                except Exception:
                    results.append(str(r.rdata))

        return jsonify({
            "domain": domain,
            "type": record_type,
            "answers": results
        })

    except Exception as e:
        return jsonify({"domain": domain, "type": record_type, "error": str(e)}), 500


@dns_bp.route("/reverse")
def reverse():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip' parameter"}), 400

    try:
        reversed_ip = '.'.join(reversed(ip.split('.'))) + '.in-addr.arpa'
        pkt = IP(dst="8.8.8.8") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname=reversed_ip, qtype="PTR"))
        resp = sr1(pkt, verbose=0, timeout=2)

        if resp and resp.haslayer(DNS) and resp[DNS].ancount > 0:
            ptr_record = resp[DNS].an.rdata.decode()
            return jsonify({"ip": ip, "hostname": ptr_record})
        else:
            return jsonify({"ip": ip, "hostname": None, "status": "not found"})

    except Exception as e:
        return jsonify({"ip": ip, "error": str(e)}), 500


@dns_bp.route("/whois")
def whois_lookup():
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Missing 'domain' parameter"}), 400

    try:
        w = whois.whois(domain)
        return jsonify({
            "domain": domain,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "emails": w.emails
        })
    except Exception as e:
        return jsonify({"domain": domain, "error": str(e)}), 500
