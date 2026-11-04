def format_matrix(matrix):
    lines = [str([round(x, 2) for x in row]) for row in matrix]
    return "\n".join(lines)


def format_result_file(result_path):
    """Прочитать результат из JSON и подготовить текст вывода."""
    from src.json_exchange import read_message

    payload = read_message(result_path)
    matrix = payload.get("matrix")
    positive_count = payload.get("positive_count")

    if not isinstance(matrix, list) or not all(
        isinstance(row, list) for row in matrix
    ):
        raise ValueError("Результат должен содержать матрицу.")

    if type(positive_count) is not int or positive_count < 0:
        raise ValueError("Некорректное количество положительных элементов.")

    return (
        f"\nМатрица:\n{format_matrix(matrix)}\n\n"
        f"Количество положительных элементов: {positive_count}"
    )
