from flask import Blueprint

from netscan_app.api.auth import auth_bp
from netscan_app.api.dns import dns_bp
from netscan_app.api.scan import scan_bp
from netscan_app.api.web import web_bp
from netscan_app.api.utils import utils_bp

# Main versioned API blueprint
api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Register all feature blueprints under /api/v1
api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(dns_bp)
api_v1.register_blueprint(scan_bp)
api_v1.register_blueprint(web_bp)
api_v1.register_blueprint(utils_bp)
