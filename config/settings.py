import os
from pathlib import Path
from dotenv import load_dotenv

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")


class Settings:

    def __init__(self):

        self.APP_NAME = os.getenv(
            "APP_NAME", "ProductionAutomationFramework"
        )

        self.APP_ENV = os.getenv("APP_ENV", "development")

        self.DEBUG = os.getenv(
            "DEBUG", "false"
        ).lower() == "true"

        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

        self.BROWSER = os.getenv("BROWSER", "chromium").lower()

        self.HEADLESS = os.getenv(
            "HEADLESS", "true"
        ).lower() == "true"

        self.MAX_WORKERS = int(os.getenv("MAX_WORKERS", "3"))

        self.TASK_TIMEOUT = int(os.getenv("TASK_TIMEOUT", "60"))

        # Runtime directories
        self.BASE_DIR = BASE_DIR
        self.LOG_DIR = BASE_DIR / "logs"
        self.STORAGE_DIR = BASE_DIR / "storage"

        self.validate()

        self.LOG_DIR.mkdir(exist_ok=True)
        self.STORAGE_DIR.mkdir(exist_ok=True)

    def validate(self):

        if self.APP_ENV not in [
            "development", "testing", "production"
        ]:
            raise ValueError("Invalid application environment")

        if self.LOG_LEVEL not in [
            "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
        ]:
            raise ValueError("Invalid log level")

        if self.BROWSER not in [
            "chromium", "firefox", "webkit"
        ]:
            raise ValueError("Invalid browser")

        if self.MAX_WORKERS < 1:
            raise ValueError("MAX_WORKERS must be at least 1")

        if self.TASK_TIMEOUT < 1:
            raise ValueError("TASK_TIMEOUT must be positive")

        if self.APP_ENV == "production" and self.DEBUG:
            raise ValueError("DEBUG must be disabled in production")


settings = Settings()