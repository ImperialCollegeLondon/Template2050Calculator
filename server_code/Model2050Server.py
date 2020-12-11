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
def calculate(period, phase):
    print("The inputs for this model are:\n" + "\n".join(model2050.inputs))
    print()
    print("The outputs for this model are:\n" + "\n".join(model2050.outputs))
    print()

    solution = model2050.calculate({"PERIOD": period, "PHASE": phase})
    return solution
