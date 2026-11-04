"""Обмен сообщениями через JSON-файлы."""

import json
from pathlib import Path


SCHEMA_VERSION = 1


def write_message(path, payload):
    """Сохранить данные в сообщении с версией формата."""
    if not isinstance(payload, dict):
        raise ValueError("Данные сообщения должны быть объектом.")

    message = {
        "schema_version": SCHEMA_VERSION,
        "payload": payload,
    }
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(message, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def read_message(path):
    """Прочитать JSON и проверить структуру сообщения."""
    message = json.loads(Path(path).read_text(encoding="utf-8"))

    if not isinstance(message, dict):
        raise ValueError("Сообщение должно быть JSON-объектом.")

    version = message.get("schema_version")
    if type(version) is not int or version != SCHEMA_VERSION:
        raise ValueError("Неподдерживаемая версия формата сообщения.")

    payload = message.get("payload")
    if not isinstance(payload, dict):
        raise ValueError("Поле payload должно быть объектом.")

    return payload


def request_dimensions(payload):
    """Сопоставить поля n и m с параметрами rows и columns."""
    rows = payload.get("n")
    columns = payload.get("m")

    if type(rows) is not int or type(columns) is not int:
        raise ValueError("Размеры должны быть целыми числами.")

    if rows <= 0 or columns <= 0:
        raise ValueError("Размеры должны быть больше нуля.")

    return rows, columns
