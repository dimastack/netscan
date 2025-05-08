from flask import jsonify
from netscan_app.api import api_v1


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
