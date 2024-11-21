import os

LOGGING_LEVEL: str = os.environ.get("LOGGING_LEVEL", "INFO")

POSTGRES_URI: str = os.environ.get("POSTGRES_URI", "")
