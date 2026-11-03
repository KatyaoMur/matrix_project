"""Расчёт элементов матрицы и подсчёт положительных значений."""

import math


def build_matrix(rows, columns):
    """Создать матрицу по формуле sin(i + j / 2), индексы от 1."""
    return [
        [math.sin(i + j / 2) for j in range(1, columns + 1)]
        for i in range(1, rows + 1)
    ]


def count_positive(matrix):
    """Подсчитать строго положительные элементы матрицы."""
    return sum(value > 0 for row in matrix for value in row)
