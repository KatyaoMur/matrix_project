import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.json_exchange import read_message, request_dimensions, write_message


class TestJsonExchange(unittest.TestCase):
    def test_write_and_read_message(self):
        payload = {"n": 2, "m": 3}
        with TemporaryDirectory() as folder:
            path = Path(folder) / "request.json"
            write_message(path, payload)
            self.assertEqual(read_message(path), payload)

    def test_read_message_rejects_invalid_structure(self):
        cases = (
            "[]",
            '{"schema_version": 2, "payload": {}}',
            '{"schema_version": 1, "payload": []}',
        )
        with TemporaryDirectory() as folder:
            path = Path(folder) / "request.json"
            for content in cases:
                with self.subTest(content=content):
                    path.write_text(content, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        read_message(path)

    def test_request_dimensions_accepts_positive_integers(self):
        self.assertEqual(request_dimensions({"n": 2, "m": 3}), (2, 3))

    def test_request_dimensions_rejects_non_integer_values(self):
        for n, m in ((True, 3), (2, "3"), ("2", None)):
            with self.subTest(n=n, m=m):
                with self.assertRaisesRegex(ValueError, "целыми числами"):
                    request_dimensions({"n": n, "m": m})

    def test_request_dimensions_rejects_non_positive_values(self):
        for n, m in ((0, 3), (2, -1), (0, 0)):
            with self.subTest(n=n, m=m):
                with self.assertRaisesRegex(ValueError, "больше нуля"):
                    request_dimensions({"n": n, "m": m})