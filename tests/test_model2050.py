import sys
from pathlib import Path

from server_code import model2050

sys.path.append(str(Path(__file__).absolute().parent / "test_model"))

import interface2050  # noqa: E402

model = model2050.Model2050(interface2050)


def output_a(factor, offset):
    xs = [i / 10 for i in range(0, 21)]
    return [x * factor + offset for x in xs]


def output_b(factor, offset):
    xs = [i / 10 for i in range(0, 21)]
    return [x ** factor + offset for x in xs]


def test_model():
    sheet_inputs = [2, 1]
    calc = model.calculate(sheet_inputs)

    assert list(calc["a"][0]) == output_a(*sheet_inputs)
    assert list(calc["b"][0]) == output_b(*sheet_inputs)

    mod_inputs = [3, 2]
    calc = model.calculate(mod_inputs)

    assert list(calc["a"][0]) == output_a(*mod_inputs)
    assert list(calc["b"][0]) == output_b(*mod_inputs)
