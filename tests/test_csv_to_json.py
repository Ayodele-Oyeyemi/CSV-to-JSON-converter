"""
Basic tests for csv_to_json.py.

Run with:
    python -m unittest discover tests
or:
    python tests/test_csv_to_json.py
"""

import sys
import tempfile
import shutil
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from csv_to_json import csv_to_json_data, infer_value


class TestInferValue(unittest.TestCase):
    def test_integer(self):
        self.assertEqual(infer_value("42"), 42)

    def test_float(self):
        self.assertEqual(infer_value("3.14"), 3.14)

    def test_true(self):
        self.assertEqual(infer_value("true"), True)
        self.assertEqual(infer_value("True"), True)

    def test_false(self):
        self.assertEqual(infer_value("false"), False)

    def test_null_variants(self):
        self.assertIsNone(infer_value(""))
        self.assertIsNone(infer_value("null"))
        self.assertIsNone(infer_value("N/A"))

    def test_plain_string(self):
        self.assertEqual(infer_value("hello"), "hello")


class TestCsvToJsonData(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def write_csv(self, filename: str, content: str) -> Path:
        path = self.tmp_dir / filename
        path.write_text(content, encoding="utf-8")
        return path

    def test_basic_conversion(self):
        csv_path = self.write_csv("basic.csv", "name,age\nAda,30\nGrace,85\n")
        data = csv_to_json_data(csv_path, delimiter=",", infer_types=False)
        self.assertEqual(
            data,
            [
                {"name": "Ada", "age": "30"},
                {"name": "Grace", "age": "85"},
            ],
        )

    def test_type_inference(self):
        csv_path = self.write_csv("typed.csv", "name,age,active\nAda,30,true\nGrace,,false\n")
        data = csv_to_json_data(csv_path, delimiter=",", infer_types=True)
        self.assertEqual(
            data,
            [
                {"name": "Ada", "age": 30, "active": True},
                {"name": "Grace", "age": None, "active": False},
            ],
        )

    def test_custom_delimiter(self):
        csv_path = self.write_csv("semicolon.csv", "name;age\nAda;30\n")
        data = csv_to_json_data(csv_path, delimiter=";", infer_types=False)
        self.assertEqual(data, [{"name": "Ada", "age": "30"}])


if __name__ == "__main__":
    unittest.main()
