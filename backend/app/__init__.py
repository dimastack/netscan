from flask import Flask
from flask_jwt_extended import JWTManager

from app.core.config import DevelopmentConfig, ProductionConfig
from app.routes.api import api_v1  # The versioned API blueprint with all sub-blueprints

config_mapping = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
jwt = JWTManager()


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_mapping.get(config_name, DevelopmentConfig))

    # Register the versioned API blueprint (includes all features)
    app.register_blueprint(api_v1)
    jwt.init_app(app)

    return app
