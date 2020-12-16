from ._anvil_designer import MainTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go


class Main(MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        
        # Can programatically add components
#         self.period_slider = ASlider(name="Period", max=5, changed=self.build_graphs)
#         self.sliders_column.add_component(self.period_slider)
#         self.period_slider.set_event_handler("changed", self.slider_changed)
        
        self.ambition_levers.items = [
            dict(name="Period", max=5, changed=self.build_graphs, min=0, step=1, value=1)
        ]
        self.build_graphs()


    def build_graphs(self, **event_args):
        print(self.ambition_levers.items[0]["value"])
        model_outputs = anvil.server.call(
            "calculate",
            self.ambition_levers.items[0]["value"],
            self.phase_slider.item["value"]
        )
        self.sin_plot.layout.title = "Sin Graph"
        self.cos_plot.layout.title = "Cos Graph"
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

    def tab_click(self, **event_args):
      """This method is called when the button is clicked"""
      tab = event_args["sender"]
      for t in tab.parent.get_components():
          t.role = ""
      tab.role = "raised"
      
      self.ambition_levers.items += [dict(name="new!")]


    def tabs_show(self, **event_args):
      """This method is called when the FlowPanel is shown on the screen"""
      self.tab_1.role = "raised"



