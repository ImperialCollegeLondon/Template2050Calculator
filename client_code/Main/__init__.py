from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go

from .AmbitionLevel import AmbitionLevel

class Main(MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.period_input.level = 1
        self.add_component(AmbitionLevel(name="Period"), slot="")
        self.sin_plot.layout.title = "Sin Graph"
        self.cos_plot.layout.title = "Cos Graph"
        self.build_graphs()

    def build_graphs(self):
        model_outputs = anvil.server.call(
            "calculate", self.period_input.level, self.phase_level.value
        )
        self.sin_plot.data = go.Scatter(
            x=model_outputs["X"][0],
            y=model_outputs["SIN"][0],
            mode="lines",
            name="sin",
        )
        self.cos_plot.data = go.Scatter(
            x=model_outputs["X"][0],
            y=model_outputs["COS"][0],
            mode="lines",
            name="cos",
        )

    def period_input_change(self, level, **event_args):
      """This method is called when the slider is moved"""
      self.period_value.text = level
      self.build_graphs()

    def phase_level_changed(self, **event_args):
      """This method is called Value of slider changed"""
      self.build_graphs()


