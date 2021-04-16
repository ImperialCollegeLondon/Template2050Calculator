import re
from collections import OrderedDict
from functools import partial

import numpy as np

SETTER_REGEX = re.compile("set_(?P<sheet>\\S*)_(?P<col>[a-z]+)(?P<row>\\d+)")
GETTER_REGEX = re.compile("output_(?P<name>\\S*)")


class Model2050:
    """A wrapper class for compiled 2050 Calculator models produced by excel_to_code
    and wrapped with SWIG. Provides a simple interface for running the model."""

    def __init__(self, module):
        """`module` should be Python module produced by SWIG to be wrapped."""
        self.module = module

        # Extract setter functions that control model input levers. Order by the
        # row in which they appear in the sheet and wrap them so they're easy to
        # call
        setter_matches = list(self._iter_matching_names(module, SETTER_REGEX))
        setter_matches.sort(key=lambda match: float(match.groupdict()["row"]))

        # extract getter functions that contain output data
        getter_matches = list(self._iter_matching_names(module, GETTER_REGEX))
        self.outputs = {
            match.groupdict()["name"]: getattr(module, match.string)
            for match in getter_matches
        }

        lever_names = [
            row[0] for row in self._values_from_range(module.output_lever_names())
        ]
        self.input_levers = OrderedDict(
            (name, partial(self._set_input_lever, getattr(module, match.string)))
            for name, match in zip(lever_names, setter_matches)
        )

    def _iter_matching_names(self, module, regex):
        """Generator that yields attributes of `module` that match the provided
        `regex`"""
        for d in dir(module):
            match = regex.match(d)
            if match:
                yield match

    def calculate(self, input_values):
        """Run the model and return a dictionary containing all model
        outputs. `input_values` should be a sequence returing valid values for
        each input lever of the model i.e. 1 to 4.

        """
        assert len(input_values) == len(self.input_levers)

        self.module.reset()

        for func, value in zip(self.input_levers.values(), input_values):
            assert value in (1, 2, 3, 4)
            func(value)

        return {
            name: self._values_from_range(output())
            for name, output in self.outputs.items()
        }

    def _set_input_lever(self, func, value):
        """Wrapper function that creates an appropriate input datatype to interact with
        the model library."""
        ev = self.module.excel_value()
        ev.type = self.module.ExcelNumber
        ev.number = value
        func(ev)

    def input_values_default(self):
        """Return a valid input for `self.calculate` with all levers set to 1."""
        return np.ones(len(self.input_levers))

    def _values_from_range(self, excel_range):
        """Wrapper function that converts the model library output datatype to a nested
        list."""
        cells = [
            [
                self.module.get_cell(excel_range, j * excel_range.columns + i)
                for i in range(excel_range.columns)
            ]
            for j in range(excel_range.rows)
        ]

        values = [
            [
                cell.number if cell.type == self.module.ExcelNumber else cell.string
                for cell in row
            ]
            for row in cells
        ]
        return values
