import unittest
import os
from unittest.mock import patch

from security import SecurityManager


class TestSecurityManager(unittest.TestCase):

    def setUp(self):
        self.security = SecurityManager()

    def test_environment_validation(self):
        with patch.dict(os.environ, {
            "APP_NAME": "TestApp",
            "APP_ENV": "development",
            "LOG_LEVEL": "INFO"
        }):
            self.assertTrue(
                self.security.validate_environment()
            )

    def test_url_validation(self):
        self.assertTrue(
            self.security.validate_url("https://example.com")
        )
        self.assertFalse(
            self.security.validate_url("invalid-url")
        )

    def test_token_generation(self):
        token = self.security.generate_token()
        self.assertTrue(token)
        self.assertGreater(len(token), 20)

    def test_input_sanitization(self):
        self.assertEqual(
            self.security.sanitize_input("  Hello  "),
            "Hello"
        )
        self.assertEqual(
            self.security.sanitize_input(123),
            ""
        )

    def test_production_mode(self):
        with patch.dict(os.environ, {"APP_ENV": "production"}):
            self.assertTrue(
                self.security.check_production_mode()
            )


if __name__ == "__main__":
    unittest.main()