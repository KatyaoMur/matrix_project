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


def process_request(request_path, result_path):
    """Прочитать задание, выполнить расчёт и сохранить результат."""
    from src.json_exchange import (
        read_message,
        request_dimensions,
        write_message,
    )

    payload = read_message(request_path)
    rows, columns = request_dimensions(payload)
    matrix = build_matrix(rows, columns)

    write_message(
        result_path,
        {
            "matrix": matrix,
            "positive_count": count_positive(matrix),
        },
    )
