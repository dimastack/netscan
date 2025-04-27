from flask import Blueprint, jsonify

api_v1_bp = Blueprint("api", __name__)

@api_v1_bp.route("/auth")
def api_test():
    return jsonify({"message": "API route OK"})
