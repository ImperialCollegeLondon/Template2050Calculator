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
    return [
        "UK Transport Demand",
        "International Aviation",
        "Light Vehicles - Electric",
        "Light Vehicles - Hydrogen",
        "Light Vehicles - Hybrid",
        "Light Vehicles - Biofuel",
        "Heavy Vehicles - Electric",
        "Heavy Vehicles - Hydrogen",
        "Heavy Vehicles - Hybrid",
        "Heavy Vehicles - Biofuel",
        "Aviation Efficiency",
        "Aviation Biofuel",
        "Buildings Temperature",
        "Buildings Insulation",
        "District Heat Share",
        "Heat Pump Share",
        "Hybrid Heat Share",
        "Network - Heat Pump",
        "Heat Network - Biomass",
        "Lighting and Appliances",
        "Industrial Efficiency",
        "Industry Electrification",
        "Industry Shift to Biomass",
        "Industry Shift to Gas",
        "Industry CCS",
        "Hydrogen Gas Grid Share",
        "Biomethane Gas Grid Share",
        "Hydrogen - Biomass CCS",
        "Hydrogen - Methane CCS",
        "Hydrogen - Imports",
        "Greenhouse Gas Removal",
        "Bio-Conversion with CCS",
        "CCS Capture Rate",
        "Seasonal Storage",
        "Short Term Balancing",
        "Biomass with CCS",
        "Nuclear",
        "Offshore & Onshore Wind",
        "Solar",
        "Wave & Tidal",
        "Gas with CCS",
        "Farming Yield & Efficiency",
        "Forestry",
        "Land for Bioenergy",
        "Waste Reduction",
    ]


@anvil.server.callable
def outputs():

    return list(model.outputs.keys())


@anvil.server.callable
def calculate(inputs):
    solution = model.calculate(inputs)
    solution["emissions_sector"] = solution["emissions_sector"][-4::-1, 1:9]
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
