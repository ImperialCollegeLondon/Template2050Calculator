from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server

from .FiguresPanel import FiguresPanel
from .. import Model


class Main(MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        
        self.ambition_levers.items = [
            {"name": name.title()} for name in Model.inputs
        ]
        self.ambition_levers.set_event_handler("x-refresh", self.update_graphs)
        self.select_figures()
        self.update_graphs()

    def select_figures(self):
        self.figures_panel = FiguresPanel()
        self.plot_area.clear()
        self.plot_area.add_component(self.figures_panel)

    def update_graphs(self, **event_args):
        inputs = {item["name"]: item["value"] for item in self.ambition_levers.items}
        self.figures_panel.calculate(**inputs)
