import os
try:
    from dotenv import load_dotenv
except ImportError:  # Running without a .env file should still work for this assignment.
    def load_dotenv():
        return False

load_dotenv()


class Config:
    """Application configuration."""

    APP_NAME = " Mini Scheduling System"

    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV == "development"

    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 3000))

    APPROVAL_MODE = os.getenv("APPROVAL_MODE", "auto")
    DEFAULT_TIMEZONE = os.getenv("DEFAULT_TIMEZONE", "UTC")

    JSON_DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
