import anvil.server

import i18n

from . import interface2050
from .model2050 import Model2050

model = Model2050(interface2050)


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
i18n.load_path.append("./Template2050Calculator/server_code/translations")


@anvil.server.callable
def translate(locale, text):
    i18n.set("locale", locale)
    return i18n.t(text)


# from openpyxl import load_workbook

# wb = load_workbook(
#     filename="../UK_Pathways_Calculator_Model_Development_Climact_200703_publ_template.xlsm"
# )
# ws = wb["WebOutputs"]

# web_outputs = {}
# for col in ws.iter_cols(3, 14, 31, 68, values_only=True):
#     web_outputs[col[0]] = col[1:]

# print(web_outputs.keys())


@anvil.server.callable
def web_outputs_keys():
    import json
    from pathlib import Path

    with open(Path("Template2050Calculator").absolute() / "web_outputs.json") as f:
        data = json.load(f)

    return data
