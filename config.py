import os


class Config:
    """Configuration management for Flask application
    All config values can be overridden via environment variables
    """

    IP_API_URL = os.getenv("IP_API_URL", "http://ip-api.com/json")
    IPIFY_URL = os.getenv("IPIFY_URL", "https://api.ipify.org?format=json")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PORT = int(os.getenv("PORT", 8001))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
