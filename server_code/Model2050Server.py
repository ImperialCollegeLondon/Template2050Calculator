import anvil.server
from pathlib import Path

from .model2050 import Model2050

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:

fpath = Path(__file__).parent / "test.xlsx"

model2050 = Model2050(fpath)


@anvil.server.callable
def inputs():
    return model2050.inputs


@anvil.server.callable
def outputs():
    return model2050.outputs


@anvil.server.callable
def calculate(inputs):
    solution = model2050.calculate(inputs)
    return solution
