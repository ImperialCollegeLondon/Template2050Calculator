from ._anvil_designer import SinGraphTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go


class SinGraph(SinGraphTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.period_input.text = 1
        self.phase_input.text = 0
        self.sin_plot.layout.title = "Sin Graph"
        self.cos_plot.layout.title = "Cos Graph"
        self.build_graphs()

    def build_graphs(self):
        model_outputs = anvil.server.call(
            "calculate", self.period_input.text, self.phase_input.text
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

    def build_graph_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.build_graphs()

    def period_input_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.build_graphs()

    def phase_input_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.build_graphs()
