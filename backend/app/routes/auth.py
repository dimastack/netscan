from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db_session
from app.models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["POST"])
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


@auth_bp.route("/login", methods=["POST"])
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


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """
    Retrieve the authenticated user's ID.

    Request Headers:
        Authorization (str): A valid JWT token in the form of 'Bearer <access_token>'.

    Returns:
        JSON with the authenticated user's ID.
    """

    user_id = int(get_jwt_identity())
    return jsonify({"user_id": user_id})
