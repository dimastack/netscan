import jwt

from functools import wraps
from flask import Blueprint, request, jsonify

from netscan_app.core.config import Config


# Decorator to require token validation
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 401

        try:
            # Extract the token and verify it
            token = token.split(" ")[1]
            decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            # Store the decoded token in request for use in other functions
            request.user = decoded_token
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token!'}), 401

        return f(*args, **kwargs)

    return decorated_function


validate_token_bp = Blueprint('validate_token', __name__)

@validate_token_bp.route('/validate-token', methods=['GET'])
@token_required
def validate_token():
    """
    Endpoint to validate the user's JWT token.
    Returns:
        - `200 OK` if token is valid.
        - `401 Unauthorized` if token is invalid or expired.
    """
    return jsonify({'valid': True}), 200
