from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from app.core.db import db_session
from app.models.user_model import User

register_bp = Blueprint("register", __name__)

@register_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user with a username, email, and password.

    Request Body:
        username (str): The desired username (required).
        email (str): The desired email (required).
        password (str): The desired password (required).

    Returns:
        JSON with a success message if the user is registered successfully.
        If the username or email is already in use, returns an error message.
    """
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing username, email, or password"}), 400

    with db_session() as session:
        if session.query(User).filter_by(email=email).first():
            return jsonify({"error": "Email already in use"}), 409
        if session.query(User).filter_by(username=username).first():
            return jsonify({"error": "Username already taken"}), 409

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        session.add(user)

    return jsonify({"message": "User registered successfully"}), 201
