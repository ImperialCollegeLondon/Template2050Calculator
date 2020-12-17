from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server

from .FiguresPanel import FiguresPanel

class Main(MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        
        # Can programatically add components
#         self.period_slider = ASlider(name="Period", max=5, changed=self.build_graphs)
#         self.sliders_column.add_component(self.period_slider)
#         self.period_slider.set_event_handler("changed", self.slider_changed)
        self.select_figures()
        self.ambition_levers.items = [
            dict(name="Period", max=5),
            dict(name="Phase", min=0,  value=0),
        ]
        self.ambition_levers.set_event_handler("x-refresh", self.update_graphs)
        self.update_graphs()

    def select_figures(self):
        self.panel = FiguresPanel()
        self.plot_area.clear()
        self.plot_area.add_component(self.panel)
        
    def update_graphs(self, **event_args):
        period = self.ambition_levers.items[0]["value"],
        phase = self.ambition_levers.items[1]["value"]
        self.panel.recalculate(period, phase)


        
