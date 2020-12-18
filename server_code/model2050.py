import re
from collections import namedtuple

import formulas

REFERENCE_REGEX = re.compile(
    "'\\[(?P<book>\\S*)\\](?P<sheet>\\S*)'!(?P<range>[A-Z,\\d,:]*)"
)
NAMED_REFERENCE_REGEX = re.compile("'\\[(?P<book>\\S*)\\]'!(?P<name>\\S*)")


def range_name(range_obj):
    return range_obj.ranges[0]["name"]


def remove_name_prefix(name):
    return name.upper().removeprefix("INPUT.").removeprefix("OUTPUT.")


Reference = namedtuple("Reference", ("book", "sheet", "range"))
NamedReference = namedtuple("NamedReference", ("book", "name"))


def split_reference(reference):
    return Reference(**REFERENCE_REGEX.match(reference).groupdict())


def split_named_reference(named_reference):
    return NamedReference(**NAMED_REFERENCE_REGEX.match(named_reference).groupdict())


class Model2050:
    def __init__(self, xlsx_path):
        self.model = formulas.ExcelModel().loads(str(xlsx_path)).finish()
        self.book = xlsx_path.name

    def make_reference(self, sheet, range_):
        return f"'[{self.book.upper()}]{sheet.upper()}'!{range_.upper()}"

    def make_named_reference(self, name):
        return f"'[{self.book.upper()}]'!{name.upper()}"

    @property
    def inputs(self):
        return self._patterns("input")

    def _reference_by_name(self, name, references):
        try:
            return [inp for inp in references if inp.name.lower() == name.lower()][0]
        except IndexError:
            raise ValueError("Could not find reference with that name")

    def input_by_name(self, name):
        return self._reference_by_name(name, self.inputs)

    def output_by_name(self, name):
        return self._reference_by_name(name, self.outputs)

    @property
    def outputs(self):
        return self._patterns("output")

    def _patterns(self, root):
        return [
            remove_name_prefix(split_named_reference(ref).name)
            for ref in self.model.references
            if split_named_reference(ref).name.lower().startswith(root.lower())
        ]

    def calculate(self, inputs):
        solution = self.model.calculate(
            inputs={
                range_name(
                    self.model.references[self.make_named_reference("input." + key)]
                ): value
                for key, value in inputs.items()
            }
        )
        return {
            output: solution[self.make_named_reference("OUTPUT." + output)].value
            for output in self.outputs
        }
