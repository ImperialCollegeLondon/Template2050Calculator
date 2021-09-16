import re

import numpy as np

GETTER_REGEX = re.compile(r"(?P<name>output_\S*)")


class Model2050:
    """A wrapper class for compiled 2050 Calculator models produced by excel_to_code
    and wrapped with SWIG. Provides a simple interface for running the model."""

    def __init__(self, module):
        """`module` should be Python module produced by SWIG to be wrapped."""
        self.module = module

        # Wrap required input functions
        self.lever_ambition = self._wrap_input_function(module.set_input_lever_ambition)
        self.lever_start = self._wrap_input_function(module.set_input_lever_start)
        self.lever_end = self._wrap_input_function(module.set_input_lever_end)

        self.start_values_default = self._wrap_output_function_1d(
            module.input_lever_start
        )
        self.end_values_default = self._wrap_output_function_1d(module.input_lever_end)

        # extract getter functions that contain output data and wrap them for
        # convenience
        getter_matches = list(self._iter_matching_names(module, GETTER_REGEX))
        self.outputs = {
            match.groupdict()["name"]: self._wrap_output_function(
                getattr(module, match.string)
            )
            for match in getter_matches
        }

        self.number_of_levers = len(self.outputs["output_lever_names"]())

    def _iter_matching_names(self, module, regex):
        """Generator that yields attributes of `module` that match the provided
        `regex`"""
        for d in dir(module):
            match = regex.match(d)
            if match:
                yield match

    def calculate(self, ambition_values, start_values=None, end_values=None):
        """Run the model and return a dictionary containing all model
        outputs. `ambition_values` should be a sequence returing valid values
        for each input lever of the model i.e. 1 to 4. `start_values` and
        `end_values` should provide a sequence of integer values representing
        years up to 2100 for each input lever. If no keyword arguments are
        provided model defaults are used instead.
        """

        self.module.reset()

        self._check_input_values(ambition_values, "ambition")
        self.lever_ambition(ambition_values)

        if start_values:
            self._check_input_values(start_values, "start")
            self.lever_start(start_values)

        if end_values:
            self._check_input_values(end_values, "end")
            self.lever_end(end_values)

        return {name: output() for name, output in self.outputs.items()}

    def _check_input_values(self, values, lever_type):
        """Validate number of input `values` and their ranges based on `lever_type`"""
        if len(values) != self.number_of_levers:
            raise ValueError(
                f"Number of {lever_type} values does not match number of levers"
            )
        if lever_type == "ambition":
            lower_limit, upper_limit = 1, 4
        else:
            lower_limit, upper_limit = 2015, 2100

        if any([not (lower_limit <= value <= upper_limit) for value in values]):
            raise ValueError(f"Input value out of range for {lever_type} values")

    def _wrap_input_function(self, func):
        """Wrap a model input `func` that expects a column of cells so it may be called
        with a list values.
        """

        def wrapper(values):
            ev = self.module.excel_value()
            ev.type = self.module.ExcelRange
            ev.columns = 1
            ev.rows = len(values)

            # create_range performs memory allocation
            self.module.create_range(ev, len(values))
            for i, value in enumerate(values):
                self.module.set_cell(ev, i, value)
            func(ev)

            # free allocated memory
            self.module.destroy_range(ev)

        return wrapper

    def _wrap_output_function(self, func):
        """Wrap a model output `func` such that values are returned as a 2-d nested
        list.
        """

        def wrapper():
            return self._values_from_range(func())

        return wrapper

    def _wrap_output_function_1d(self, func):
        """Wrap a model output `func` such that values are returned as a list."""

        def wrapper():
            return [v[0] for v in self._values_from_range(func())]

        return wrapper

    def input_values_default(self):
        """Return a valid input for `self.calculate` with all levers set to 1."""
        return np.ones(self.number_of_levers)

    def _values_from_range(self, excel_range):
        """Convenience function that converts the model library output datatype to a
        nested list.
        """
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
