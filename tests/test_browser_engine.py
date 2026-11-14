import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(r"C:\playwright-project")
sys.path.insert(0, str(PROJECT_ROOT))

from main import Browser


class TestBrowserEngine(unittest.TestCase):

    def setUp(self):
        self.browser = Browser()

    def test_browser_initialization(self):
        self.assertIsNone(self.browser.playwright)
        self.assertIsNone(self.browser.browser)
        self.assertIsNone(self.browser.context)
        self.assertIsNone(self.browser.page)

    def test_valid_http_url(self):
        self.assertTrue(
            self.browser.is_valid_url("http://example.com")
        )

    def test_valid_https_url(self):
        self.assertTrue(
            self.browser.is_valid_url("https://example.com")
        )

    def test_invalid_url(self):
        self.assertFalse(
            self.browser.is_valid_url("example.com")
        )

    def test_invalid_url_without_protocol(self):
        self.assertFalse(
            self.browser.is_valid_url("www.example.com")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)