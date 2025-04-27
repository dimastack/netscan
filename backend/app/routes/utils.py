from flask import Blueprint, request, jsonify
from app.utils.net import resolve_hostname, reverse_dns, check_latency, get_http_headers

utils_bp = Blueprint("utils", __name__)


@utils_bp.route("/resolve")
def resolve():
    host = request.args.get("host")
    if not host:
        return jsonify({"error": "Missing 'host' parameter"}), 400
    return jsonify(resolve_hostname(host))


@utils_bp.route("/reverse")
def reverse():
    ip = request.args.get("ip")
    if not ip:
        return jsonify({"error": "Missing 'ip' parameter"}), 400
    return jsonify(reverse_dns(ip))


@utils_bp.route("/latency")
def latency():
    host = request.args.get("host")
    port = request.args.get("port", default=80, type=int)
    if not host:
        return jsonify({"error": "Missing 'host' parameter"}), 400
    return jsonify(check_latency(host, port))


@utils_bp.route("/headers")
def headers():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400
    return jsonify(get_http_headers(url))
