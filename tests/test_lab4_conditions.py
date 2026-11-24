import pytest

from src.json_exchange import read_message, write_message
from src.matrix_sin import process_request


@pytest.mark.parametrize(
    ("rows", "columns", "expected_valid"),
    [
        (1, 1, True),
        (0, 1, False),
        (1, 0, False),
        (0, 0, False),
    ],
)
def test_dimension_conditions(tmp_path, rows, columns, expected_valid):
    request = tmp_path / "request.json"
    result = tmp_path / "result.json"
    write_message(request, {"n": rows, "m": columns})

    if expected_valid:
        process_request(request, result)
        assert read_message(result)["positive_count"] == 1
    else:
        with pytest.raises(ValueError):
            process_request(request, result)

        assert not result.exists()
