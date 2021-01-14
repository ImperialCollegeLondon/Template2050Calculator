import anvil.server

from . import interface2050
from .model2050 import Model2050

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:

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
