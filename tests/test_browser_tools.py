import sys
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE6_PATH = Path(r"C:\playwright-project\module6-agent")
sys.path.insert(0, str(MODULE6_PATH))

from tools import BrowserTools


class TestBrowserTools(unittest.TestCase):

    def setUp(self):
        with patch.object(Path, "mkdir"):
            self.tools = BrowserTools()

    def test_initialization(self):
        self.assertEqual(self.tools.browser_type, "chromium")
        self.assertEqual(self.tools.timeout, 30000)
        self.assertEqual(self.tools.profile_name, "default")

    def test_profile_path(self):
        self.assertEqual(
            self.tools.get_profile_path(),
            Path("memory_profiles/default.json")
        )

    def test_set_memory_profile(self):
        self.tools.set_memory_profile("user1")
        self.assertEqual(self.tools.profile_name, "user1")

    def test_invalid_memory_profile(self):
        with self.assertRaises(ValueError):
            self.tools.set_memory_profile("../invalid")

    def test_browser_memory_without_context(self):
        with self.assertRaises(RuntimeError):
            self.tools.get_browser_memory()


if __name__ == "__main__":
    unittest.main(verbosity=2)