from flask import Blueprint, jsonify

from app.routes.auth import auth_bp
from app.routes.dns import dns_bp
from app.routes.scan import scan_bp
from app.routes.web import web_bp
from app.routes.utils import utils_bp

# Main versioned API blueprint
api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

# Register all feature blueprints under /api/v1
api_v1.register_blueprint(auth_bp)
api_v1.register_blueprint(dns_bp)
api_v1.register_blueprint(scan_bp)
api_v1.register_blueprint(web_bp)
api_v1.register_blueprint(utils_bp)


@api_v1.route("/", methods=["GET"])
def index():
    """
    Return a simple welcome message for the API.

    This route serves as a root endpoint for the API, typically used for
    checking if the API is accessible.

    Returns:
        JSON with a welcome message or basic API information.
    """ 

    return jsonify({
        "message": "Welcome to NetScan API v1",
        "status": "ok"
    })
