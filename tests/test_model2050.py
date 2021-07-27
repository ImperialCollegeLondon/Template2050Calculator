import sys
from pathlib import Path

from pytest import approx, mark, raises

from server_code import model2050

sys.path.append(str(Path(__file__).absolute().parent / "test_model"))

import interface2050  # noqa: E402

model = model2050.Model2050(interface2050)


def output_a(ambition, start, end):
    factor, offset = ambition
    xs = [i / 10 for i in range(0, 21)]
    return [x * factor + offset + start[0] - end[0] for x in xs]


def output_b(ambition, start, end):
    factor, offset = ambition
    xs = [i / 10 for i in range(0, 21)]
    return [x ** factor + offset + start[1] - end[1] for x in xs]


@mark.parametrize(
    "ambition,start,end",
    [
        [  # spreadsheet defaults for all
            [2, 1],
            None,
            None,
        ],
        [  # vary lever ambition inputs
            [3, 2],
            None,
            None,
        ],
        [  # vary lever start inputs
            [2, 1],
            [2020, 2025],
            None,
        ],
        [  # vary lever end inputs
            [2, 1],
            None,
            [2020, 2025],
        ],
    ],
)
def test_model(ambition, start, end):

    calc = model.calculate(ambition, start, end)

    start = [1, 2] if not start else start
    end = [1, 2] if not end else end

    assert list(calc["output_a"][0]) == approx(output_a(ambition, start, end), 7)
    assert list(calc["output_b"][0]) == approx(output_b(ambition, start, end), 7)


@mark.parametrize(
    "ambition,start,end",
    [
        [  # too many ambition values
            [1, 1, 1],
            None,
            None,
        ],
        [  # too many start values
            [1, 1],
            [1, 1, 1],
            None,
        ],
        [  # too many end values
            [1, 1],
            None,
            [1, 1, 1],
        ],
        [  # ambition value out of range
            [0.5, 1],
            None,
            None,
        ],
        [  # start value out of range
            [1, 1],
            [2000, 2020],
            None,
        ],
        [  # end value out of range
            [1, 1],
            None,
            [2000, 2020],
        ],
    ],
)
def test_invalid_inputs(ambition, start, end):
    with raises(ValueError):
        model.calculate(ambition, start, end)


def test_default_values():
    assert model.start_values_default() == [2050.0, 2050.0]
    assert model.end_values_default() == [2050.0, 2050.0]
