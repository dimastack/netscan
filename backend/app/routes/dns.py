from flask import Blueprint, jsonify

dns_bp = Blueprint("dns", __name__)

@dns_bp.route("/test")
def dns_test():
    return jsonify({"message": "DNS route OK"})
