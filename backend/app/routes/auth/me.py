from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

me_bp = Blueprint("me", __name__)

@me_bp.route("/me", methods=["GET"])
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
