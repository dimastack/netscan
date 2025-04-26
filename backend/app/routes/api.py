from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__)

@api_bp.route("/auth")
def api_test():
    return jsonify({"message": "API route OK"})
