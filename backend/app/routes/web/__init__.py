from flask import Blueprint

from .httpcheck import httpcheck_bp
from .sslcheck import sslcheck_bp

web_bp = Blueprint("web", __name__, url_prefix="/web")

web_bp.register_blueprint(httpcheck_bp)
web_bp.register_blueprint(sslcheck_bp)
