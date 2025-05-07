import whois
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.core.db import db_session
from app.models.scan_results import ScanResult

whois_bp = Blueprint("whois", __name__)


@whois_bp.route("/whois")
@jwt_required()
def whois_lookup():
    """
    Perform a WHOIS lookup for a domain.

    Query Parameters:
        domain (str): The domain name to look up WHOIS information for.

    Returns:
        JSON with WHOIS data such as registrar, creation/expiration dates, name servers, and contact email.
    """

    user_id = int(get_jwt_identity())

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
