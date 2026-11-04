"""Запуск расчётного модуля с ограничением времени."""

import os
from pathlib import Path
import subprocess
import sys


def run_calculation(
    request_path,
    result_path,
    timeout=5,
    worker_module="src.worker",
):
    request = Path(request_path).resolve()
    result = Path(result_path).resolve()
    project_root = Path(__file__).resolve().parents[1]
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "utf-8"

    command = [
        sys.executable,
        "-m",
        worker_module,
        str(request),
        str(result),
    ]

    try:
        subprocess.run(
            command,
            cwd=project_root,
            env=environment,
            timeout=timeout,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except subprocess.TimeoutExpired as error:
        raise TimeoutError(
            "Превышено время ожидания расчётного модуля."
        ) from error
    except subprocess.CalledProcessError as error:
        details = error.stderr.strip()
        raise RuntimeError(
            f"Расчётный модуль недоступен или завершился с ошибкой: {details}"
        ) from error
    except OSError as error:
        raise RuntimeError(
            f"Не удалось запустить расчётный модуль: {error}"
        ) from error
