from flask import Blueprint

from .resolve import resolve_bp
from .reverse import reverse_bp
from .latency import latency_bp
from .headers import headers_bp

utils_bp = Blueprint("utils", __name__, url_prefix="/utils")

utils_bp.register_blueprint(resolve_bp)
utils_bp.register_blueprint(reverse_bp)
utils_bp.register_blueprint(latency_bp)
utils_bp.register_blueprint(headers_bp)
