import json
from pathlib import Path


def test_get_weboutputs():
    from openpyxl import load_workbook

    from scripts.get_weboutputs import get_weboutputs

    test_model_path = Path(__file__).absolute().parent / "test_model"

    wb = load_workbook(
        filename=test_model_path / "mockay_calculator.xlsx",
        data_only=True,
        read_only=True,
        keep_vba=False,
    )

    actual = get_weboutputs(wb)

    with open(test_model_path / "mockay_outputs.json") as f:
        expected = json.load(f)

    assert expected == actual
