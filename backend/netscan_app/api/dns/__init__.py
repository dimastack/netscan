from flask import Blueprint

from .lookup import lookup_bp
from .reverse import reverse_bp
from .whois import whois_bp

dns_bp = Blueprint("dns", __name__, url_prefix="/dns")

dns_bp.register_blueprint(lookup_bp)
dns_bp.register_blueprint(reverse_bp)
dns_bp.register_blueprint(whois_bp)