"""Проверки отказов модулей и несовместимых сообщений."""

import json
import subprocess
import sys

import pytest

import src.integration_runner as runner
import src.main as app
from src.json_exchange import read_message, write_message
from src.worker import main as worker_main


@pytest.mark.parametrize(
    "message",
    [
        [],
        {"schema_version": 2, "payload": {}},
        {"schema_version": True, "payload": {}},
        {"schema_version": 1, "payload": []},
    ],
)
def test_reject_invalid_message(tmp_path, message):
    path = tmp_path / "message.json"
    path.write_text(json.dumps(message), encoding="utf-8")

    with pytest.raises(ValueError):
        read_message(path)


def test_unavailable_module(tmp_path):
    request = tmp_path / "request.json"
    result = tmp_path / "result.json"
    write_message(request, {"n": 3, "m": 3})

    with pytest.raises(RuntimeError, match="недоступен"):
        runner.run_calculation(
            request,
            result,
            worker_module="src.nonexistent_worker",
        )

    assert not result.exists()


def test_real_process_timeout(tmp_path, monkeypatch):
    original_run = subprocess.run

    def run_slow_process(command, **kwargs):
        slow_command = [
            sys.executable,
            "-c",
            "import time; time.sleep(5)",
        ]
        return original_run(slow_command, **kwargs)

    monkeypatch.setattr(runner.subprocess, "run", run_slow_process)

    with pytest.raises(TimeoutError, match="время ожидания"):
        runner.run_calculation(
            tmp_path / "request.json",
            tmp_path / "result.json",
            timeout=0.05,
        )

    assert not (tmp_path / "result.json").exists()


def test_process_launch_error(tmp_path, monkeypatch):
    def fail_to_start(*args, **kwargs):
        raise OSError("Запуск процесса запрещён")

    monkeypatch.setattr(runner.subprocess, "run", fail_to_start)

    with pytest.raises(RuntimeError, match="Не удалось запустить"):
        runner.run_calculation(
            tmp_path / "request.json",
            tmp_path / "result.json",
        )


@pytest.mark.parametrize(
    "answers",
    [
        ["abc"],
        ["2.5"],
        ["0", "3"],
        ["3", "-2"],
    ],
)
def test_main_invalid_input(tmp_path, monkeypatch, capsys, answers):
    monkeypatch.chdir(tmp_path)
    values = iter(answers)
    monkeypatch.setattr("builtins.input", lambda prompt: next(values))

    assert app.main() == 1
    assert "Ошибка:" in capsys.readouterr().out
    assert not (tmp_path / "data/result.json").exists()


@pytest.mark.parametrize(
    "error",
    [
        RuntimeError("Расчётный модуль недоступен"),
        TimeoutError("Превышено время ожидания"),
    ],
)
def test_main_handles_module_failure(
    tmp_path, monkeypatch, capsys, error
):
    monkeypatch.chdir(tmp_path)
    values = iter(["3", "3"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(values))

    def fail_calculation(*args, **kwargs):
        raise error

    monkeypatch.setattr(app, "run_calculation", fail_calculation)

    assert app.main() == 1
    assert "Ошибка обмена данными:" in capsys.readouterr().out
    assert not (tmp_path / "data/result.json").exists()


def test_worker_entry(tmp_path, monkeypatch):
    request = tmp_path / "request.json"
    result = tmp_path / "result.json"
    write_message(request, {"n": 3, "m": 3})
    monkeypatch.setattr(
        sys,
        "argv",
        ["worker", str(request), str(result)],
    )

    assert worker_main() == 0
    assert read_message(result)["positive_count"] == 5
