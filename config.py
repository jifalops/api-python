import os

LOGGING_LEVEL: str = os.environ.get("LOGGING_LEVEL", "INFO")

POSTGRES_URI: str = os.environ.get("POSTGRES_URI", "")

NEO4J_URI: str = os.environ.get("NEO4J_URI", "")
NEO4J_PASSWORD: str = os.environ.get("NEO4J_PASSWORD", "")

STRIPE_PUBLIC_KEY: str = os.environ.get("STRIPE_PUBLIC_KEY", "")
STRIPE_SECRET_KEY: str = os.environ.get("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET: str = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
