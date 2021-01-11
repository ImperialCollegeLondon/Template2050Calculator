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
    return [f"Lever {n}" for n, _ in enumerate(model.input_levers)]


@anvil.server.callable
def outputs():
    return list(model.outputs.keys())


@anvil.server.callable
def calculate(inputs):
    solution = model.calculate(inputs)
    solution["emissions_sector"] = solution["emissions_sector"][-4::-1, 1:9]
    solution["X"] = list(range(2015, 2055, 5))
    return solution
