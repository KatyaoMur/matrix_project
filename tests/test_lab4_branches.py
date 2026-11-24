import runpy
import sys

import pytest

from src.json_exchange import read_message, write_message


def test_write_message_rejects_list(tmp_path):
    target = tmp_path / "request.json"

    with pytest.raises(ValueError, match="Данные сообщения должны быть объектом"):
        write_message(target, [1, 2])

    assert not target.exists()


def test_main_entry_point(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    answers = iter(["3", "3"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))
    monkeypatch.delitem(sys.modules, "src.main", raising=False)

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module("src.main", run_name="__main__")

    assert exit_info.value.code == 0
    assert "Количество положительных элементов: 5" in capsys.readouterr().out


def test_worker_entry_point(tmp_path, monkeypatch):
    request = tmp_path / "request.json"
    result = tmp_path / "result.json"

    write_message(request, {"n": 1, "m": 1})
    monkeypatch.setattr(sys, "argv", ["src.worker", str(request), str(result)])
    monkeypatch.delitem(sys.modules, "src.worker", raising=False)

    with pytest.raises(SystemExit) as exit_info:
        runpy.run_module("src.worker", run_name="__main__")

    assert exit_info.value.code == 0
    assert read_message(result)["positive_count"] == 1
