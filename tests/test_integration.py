"""Проверки взаимодействия модулей через JSON-файлы."""

import json
import math

import pytest

from src.json_exchange import read_message, write_message
from src.main import main
from src.matrix_sin import process_request
from src.report import format_result_file


@pytest.mark.parametrize(
    "rows, columns, expected_count",
    [(3, 3, 5), (1, 1, 1)],
)
def test_file_pipeline(tmp_path, rows, columns, expected_count):
    request = tmp_path / "request.json"
    result = tmp_path / "result.json"

    write_message(request, {"n": rows, "m": columns})
    process_request(request, result)
    payload = read_message(result)

    assert len(payload["matrix"]) == rows
    assert all(len(row) == columns for row in payload["matrix"])
    assert payload["matrix"][0][0] == pytest.approx(math.sin(1.5))
    assert payload["positive_count"] == expected_count

    output = format_result_file(result)
    assert "Матрица:" in output
    assert (
        f"Количество положительных элементов: {expected_count}"
        in output
    )


@pytest.mark.parametrize(
    "payload",
    [
        {"n": 0, "m": 3},
        {"n": 3, "m": -2},
        {"n": "3", "m": 3},
        {"n": 3},
    ],
)
def test_invalid_request(tmp_path, payload):
    request = tmp_path / "request.json"
    result = tmp_path / "result.json"
    write_message(request, payload)

    with pytest.raises(ValueError):
        process_request(request, result)

    assert not result.exists()


def test_broken_json(tmp_path):
    request = tmp_path / "request.json"
    result = tmp_path / "result.json"
    request.write_text("{broken json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        process_request(request, result)

    assert not result.exists()


def test_missing_request(tmp_path):
    result = tmp_path / "result.json"

    with pytest.raises(FileNotFoundError):
        process_request(tmp_path / "missing.json", result)

    assert not result.exists()


def test_main_pipeline(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    answers = iter(["3", "3"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    assert main() == 0

    output = capsys.readouterr().out
    assert "Количество положительных элементов: 5" in output
    assert read_message(tmp_path / "data/request.json") == {
        "n": 3,
        "m": 3,
    }
    result = read_message(tmp_path / "data/result.json")
    assert result["positive_count"] == 5
