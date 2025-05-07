from flask import Blueprint

from .ping import ping_bp
from .traceroute import traceroute_bp
from .osfingerprint import osfingerprint_bp
from .portscan import portscan_bp
from .banner import banner_bp

scan_bp = Blueprint("scan", __name__)

# Register each sub-blueprint under the "scan" parent
scan_bp.register_blueprint(ping_bp)
scan_bp.register_blueprint(traceroute_bp)
scan_bp.register_blueprint(osfingerprint_bp)
scan_bp.register_blueprint(portscan_bp)
scan_bp.register_blueprint(banner_bp)