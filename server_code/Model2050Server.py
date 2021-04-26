import json
from collections import OrderedDict, namedtuple
from pathlib import Path

import anvil.server
import i18n

from . import interface2050
from .model2050 import Model2050

model = Model2050(interface2050)


with open(Path(__file__).absolute().parent.parent / "web_outputs.json") as f:
    TABLE = json.load(f)


@anvil.server.callable
def inputs():
    return model.input_values_default()


@anvil.server.callable
def levers():
    return list(model.input_levers.keys())


@anvil.server.callable
def outputs():

    return list(model.outputs.keys())


@anvil.server.callable
def calculate(inputs):
    solution = model.calculate(inputs)
    solution["emissions_sector"] = solution["emissions_sector"][-4::-1]
    solution["x"] = list(range(2015, 2055, 5))
    return solution


i18n.set("filename_format", "{locale}.{format}")
i18n.set("enable_memoization", True)
i18n.load_path.append(Path(__file__).absolute().parent / "translations")


@anvil.server.callable
def translate(locale, text):
    i18n.set("locale", locale)
    return i18n.t(text)


GraphData = namedtuple("GraphData", ("title", "output", "plot_type"))


@anvil.server.callable
def layout():
    layout = OrderedDict()
    weboutputs = TABLE["weboutputs_summary_table"]
    for tab, sub_tab, pos, title, named_range, plot_type in zip(
        weboutputs["Webtool Page"],
        weboutputs["Webtool Tab"],
        weboutputs["Position"],
        weboutputs["Title"],
        weboutputs["Named Range"],
        weboutputs["Graph Type"],
    ):

        sub_tabs = layout.setdefault(tab, OrderedDict())
        positions = sub_tabs.setdefault(sub_tab, OrderedDict())
        positions[str(pos)] = GraphData(
            title,
            named_range.replace(".", "_").removeprefix("output_").lower(),
            plot_type,
        )

    return layout


@anvil.server.callable
def lever_descriptions():
    return TABLE["lever_descriptions"]
