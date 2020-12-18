from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server

from .FiguresPanel import FiguresPanel


class Main(MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.model_inputs = anvil.server.call("inputs")
        self.model_outputs = anvil.server.call("outputs")

        self.select_figures()

        self.ambition_levers.items = [
            {"name": name.title()} for name in self.model_inputs
        ]
        self.ambition_levers.set_event_handler("x-refresh", self.update_graphs)
        self.update_graphs()

    def select_figures(self):
        self.panel = FiguresPanel()
        self.plot_area.clear()
        self.plot_area.add_component(self.panel)

    def update_graphs(self, **event_args):
        inputs = {item["name"]: item["value"] for item in self.ambition_levers.items}
        self.panel.calculate(**inputs)
