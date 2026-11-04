"""Управление модулями с обменом через JSON-файлы."""

from pathlib import Path

from src.json_exchange import write_message
from src.integration_runner import run_calculation
from src.report import format_result_file


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

    data_dir = Path("data")
    request_path = data_dir / "request.json"
    result_path = data_dir / "result.json"

    try:
        write_message(request_path, {"n": rows, "m": columns})
        run_calculation(request_path, result_path)
        output = format_result_file(result_path)
    except (OSError, ValueError, RuntimeError, TimeoutError) as error:
        print(f"Ошибка обмена данными: {error}")
        return 1

    print(output)
    print(f"\nФайл задания: {request_path}")
    print(f"Файл результата: {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
