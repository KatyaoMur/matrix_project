"""Ввод данных и управление интегрированными модулями."""

from src.matrix_sin import build_matrix, count_positive
from src.report import format_matrix


def main():
    try:
        rows = int(input("Количество строк: "))
        columns = int(input("Количество столбцов: "))
    except ValueError:
        print("Ошибка: размеры должны быть целыми числами.")
        return 1

    if rows <= 0 or columns <= 0:
        print("Ошибка: размеры должны быть больше нуля.")
        return 1

    matrix = build_matrix(rows, columns)
    positive_count = count_positive(matrix)
    formatted_matrix = format_matrix(matrix)

    print("\nМатрица:")
    print(formatted_matrix)
    print(f"\nКоличество положительных элементов: {positive_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
