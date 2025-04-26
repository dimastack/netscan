from flask import Blueprint, jsonify

utils_bp = Blueprint("utils", __name__)

@utils_bp.route("/info")
def utils_info():
    return jsonify({"message": "UTILS route OK"})
