from flask import Blueprint, request, jsonify
import whois
import dns.resolver
import dns.reversename

dns_bp = Blueprint("dns", __name__)


@dns_bp.route("/lookup")
def lookup():
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Missing 'domain' parameter"}), 400

    try:
        result = {
            "A": [r.address for r in dns.resolver.resolve(domain, 'A')],
        }

        try:
            result["AAAA"] = [r.address for r in dns.resolver.resolve(domain, 'AAAA')]
        except Exception:
            result["AAAA"] = []

        return jsonify({
            "domain": domain,
            "results": result
        })
    except Exception as e:
        return jsonify({"domain": domain, "error": str(e)}), 500


@dns_bp.route("/reverse")
def reverse():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip' parameter"}), 400

    try:
        rev_name = dns.reversename.from_address(ip)
        hostname = str(dns.resolver.resolve(rev_name, "PTR")[0])
        return jsonify({
            "ip": ip,
            "hostname": hostname
        })
    except Exception as e:
        return jsonify({
            "ip": ip,
            "error": str(e)
        }), 500


@dns_bp.route("/whois")
def whois_lookup():
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "Missing 'domain' parameter"}), 400

    try:
        w = whois.whois(domain)
        result = {
            "domain": domain,
            "registrar": w.registrar,
            "creation_date": str(w.creation_date),
            "expiration_date": str(w.expiration_date),
            "name_servers": w.name_servers,
            "emails": w.emails
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({"domain": domain, "error": str(e)}), 500
