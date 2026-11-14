import os
from dotenv import load_dotenv
load_dotenv()
import re
import secrets
import logging

logger = logging.getLogger("SecurityManager")


class SecurityManager:

    def __init__(self):
        self.secret_key = secrets.token_hex(32)
        logger.info("Security Manager Initialized")

    def validate_environment(self):
        required = ["APP_NAME", "APP_ENV", "LOG_LEVEL"]

        missing = [
            key for key in required
            if not os.getenv(key)
        ]

        if missing:
            logger.error("Missing environment variables: %s", missing)
            return False

        logger.info("Environment validation successful")
        return True

    def validate_url(self, url):
        pattern = r"^https?://[^\s]+$"

        if not re.match(pattern, url):
            logger.warning("Invalid URL rejected")
            return False

        return True

    def generate_token(self):
        return secrets.token_urlsafe(32)

    def sanitize_input(self, value):
        if not isinstance(value, str):
            return ""

        return value.strip()[:500]

    def check_production_mode(self):
        return os.getenv("APP_ENV", "development").lower() == "production"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    security = SecurityManager()

    print("Environment Valid:", security.validate_environment())
    print("URL Valid:", security.validate_url("https://example.com"))
    print("Secure Token Generated:", bool(security.generate_token()))
    print("Production Mode:", security.check_production_mode())