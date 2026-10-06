import math

from src.matrix_sin import build_matrix, count_positive
from src.report import format_matrix

def test_size_3x3():
    assert count_positive(build_matrix(3, 3)) == 5

def test_size_1x1():
    assert count_positive(build_matrix(1, 1)) == 1

def test_size_1x2():
    assert count_positive(build_matrix(1, 2)) == 2

def test_empty_matrix():
    assert count_positive(build_matrix(0, 5)) == 0

def test_shape_and_value():
    matrix = build_matrix(2, 4)
    assert len(matrix) == 2
    assert len(matrix[0]) == 4
    assert matrix[0][0] == math.sin(1.5)

def test_format_matrix():
    assert format_matrix([[1.234, 2.0]]) == "[1.23, 2.0]"

