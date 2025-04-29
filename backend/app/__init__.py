from flask import Flask
from app.config import DevelopmentConfig, ProductionConfig
from app.routes.scan import scan_bp
from app.routes.utils import utils_bp
from app.routes.dns import dns_bp
from app.routes.web import web_bp
from app.routes.api import api_bp

config_mapping = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_mapping.get(config_name, DevelopmentConfig))

    # Register blueprints with proper URL prefixes
    app.register_blueprint(scan_bp, url_prefix="/scan")
    app.register_blueprint(utils_bp, url_prefix="/utils")
    app.register_blueprint(dns_bp, url_prefix="/dns")
    app.register_blueprint(web_bp, url_prefix="/web")
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    return app
