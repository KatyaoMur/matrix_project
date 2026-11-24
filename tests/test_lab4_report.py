import unittest
from unittest.mock import patch

from src.report import format_matrix, format_result_file


class TestReport(unittest.TestCase):
    def test_format_matrix_rounds_values_and_separates_rows(self):
        result = format_matrix([[0.99749, -0.35078], [0.14112, 0.0]])
        self.assertEqual(result, "[1.0, -0.35]\n[0.14, 0.0]")

    def test_format_result_file_shows_matrix_and_count(self):
        payload = {"matrix": [[0.99749, -0.35078]], "positive_count": 1}
        with patch("src.json_exchange.read_message", return_value=payload):
            result = format_result_file("result.json")
        self.assertEqual(
            result,
            "\nМатрица:\n[1.0, -0.35]\n\nКоличество положительных элементов: 1",
        )

    def test_format_result_file_rejects_invalid_matrix(self):
        for matrix in (None, [0.5]):
            with self.subTest(matrix=matrix):
                payload = {"matrix": matrix, "positive_count": 1}
                with patch("src.json_exchange.read_message", return_value=payload):
                    with self.assertRaisesRegex(ValueError, "содержать матрицу"):
                        format_result_file("result.json")

    def test_format_result_file_rejects_invalid_count(self):
        for count in (True, -1):
            with self.subTest(count=count):
                payload = {"matrix": [[0.0]], "positive_count": count}
                with patch("src.json_exchange.read_message", return_value=payload):
                    with self.assertRaisesRegex(ValueError, "Некорректное количество"):
                        format_result_file("result.json")
