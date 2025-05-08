from flask import Blueprint

from .register import register_bp
from .login import login_bp
from .me import me_bp

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

auth_bp.register_blueprint(register_bp)
auth_bp.register_blueprint(login_bp)
auth_bp.register_blueprint(me_bp)
