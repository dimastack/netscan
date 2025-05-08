import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from the project root
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-insecure-key")
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-insecure-jwt-key")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"

    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_NAME = os.getenv("DB_NAME", "netscan_db")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    FLASK_ENV = "development"


class ProductionConfig(Config):
    FLASK_DEBUG = False
    FLASK_ENV = "production"
