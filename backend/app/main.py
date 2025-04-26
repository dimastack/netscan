from flask import Flask
from app.routes.scan import scan_bp
from app.routes.dns import dns_bp
from app.routes.utils import utils_bp
from app.routes.web import web_bp
from app.routes.api import api_v1_bp

app = Flask(__name__)

# Register Blueprints with prefixes
app.register_blueprint(scan_bp, url_prefix='/scan')
app.register_blueprint(dns_bp, url_prefix='/dns')
app.register_blueprint(utils_bp, url_prefix='/utils')
app.register_blueprint(web_bp, url_prefix='/web')
app.register_blueprint(api_v1_bp, url_prefix='/api/v1')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
