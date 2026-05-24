import unittest
from auto_gen_py_project.cli import main
from auto_gen_py_project import __version__


class TestPackage(unittest.TestCase):
    def test_version_is_string(self):
        self.assertIsInstance(__version__, str)

    def test_version_format(self):
        parts = __version__.split(".")
        self.assertGreaterEqual(len(parts), 2)
        for part in parts:
            self.assertTrue(part.isdigit(), f"Non-numeric version segment: {part}")
