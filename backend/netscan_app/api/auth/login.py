from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from netscan_app.core.db import db_session
from netscan_app.models.user import User

login_bp = Blueprint("login", __name__)

@login_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate a user and return a JWT token.

    Request Body:
        email (str): The user's email (required).
        password (str): The user's password (required).

    Returns:
        JSON with the JWT access token if the credentials are valid.
        If the credentials are invalid, returns an error message.
    """

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Missing email or password"}), 400

    with db_session() as session:
        user = session.query(User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token})
