from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go

from .AmbitionLevelSlider import AmbitionLevelSlider as ASlider

class Main(MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.sin_plot.layout.title = "Sin Graph"
        self.cos_plot.layout.title = "Cos Graph"
        
        # Can programatically add components
        self.period_slider = ASlider(name="Period", max=5, changed=self.build_graphs)
        self.sliders_column.add_component(self.period_slider)
        self.period_slider.set_event_handler("changed", self.slider_changed)
        
        self.build_graphs()
        
        self.tab_1.underline = True

    def build_graphs(self):
        model_outputs = anvil.server.call(
            "calculate", self.period_slider.value, self.phase_slider.value
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

    def slider_changed(self, **event_args):
      """This method is called when the value of the slider is changed"""
      self.build_graphs()
