from flask import Blueprint, jsonify

web_bp = Blueprint("api", __name__)

@web_bp.route("/httpcheck")
def web_httpcheck():
    return jsonify({"message": "WEB route OK"})
