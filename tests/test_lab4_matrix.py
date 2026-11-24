import unittest

from src.matrix_sin import build_matrix, count_positive


class TestMatrixSin(unittest.TestCase):
    def test_build_matrix_2_by_3(self):
        matrix = build_matrix(2, 3)
        rounded = [[round(value, 6) for value in row] for row in matrix]
        self.assertEqual(
            rounded,
            [
                [0.997495, 0.909297, 0.598472],
                [0.598472, 0.141120, -0.350783],
            ],
        )

    def test_count_positive_with_zero_and_negative_values(self):
        matrix = [[-2.0, 0.0, 1.5], [4.0, -1.0, 0.0]]
        self.assertEqual(count_positive(matrix), 2)

    def test_count_positive_in_empty_matrix(self):
        self.assertEqual(count_positive([]), 0)
