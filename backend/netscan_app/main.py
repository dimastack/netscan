import os

from netscan_app import create_app
from netscan_app.core.config import Config

# Read from env var or fallback to development
config_name = os.environ.get("FLASK_ENV", "development")
app = create_app(config_name)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=Config.FLASK_DEBUG)
