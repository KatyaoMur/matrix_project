import pytest

from src.integration_runner import run_calculation
from src.json_exchange import read_message
from src.main import main


def test_second_run_replaces_previous_result(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    answers = iter(["3", "3", "1", "1"])
    monkeypatch.setattr("builtins.input", lambda prompt: next(answers))

    result = tmp_path / "data" / "result.json"
    assert main() == 0
    assert read_message(result)["positive_count"] == 5

    assert main() == 0
    payload = read_message(result)
    assert payload["positive_count"] == 1
    assert [len(row) for row in payload["matrix"]] == [1]


def test_runner_reports_broken_json_from_worker(tmp_path):
    request = tmp_path / "request.json"
    result = tmp_path / "result.json"
    request.write_text("{broken json", encoding="utf-8")

    with pytest.raises(RuntimeError, match="Расчётный модуль недоступен"):
        run_calculation(request, result)

    assert not result.exists()
