from ._anvil_designer import FiguresPanelTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go


class FiguresPanel(FiguresPanelTemplate):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
  
      # Any code you write here will run when the form opens.
      self.trig_name = self.tab_1.text
    
    def recalculate(self, period, phase):
      self.model_outputs = anvil.server.call("calculate", period, phase-1)
      self.build_graphs()
    
    def build_graphs(self):
        self.card_1.clear()
        self.card_1.add_component(self.plot)
        # Make this server call only when updating period and phase
        # Not when changing plot. Save model_ouputs as attribute
        self.plot.layout.title = f"{self.trig_name} Graph"
        self.plot.data = go.Scatter(
            x=self.model_outputs["X"][0],
            y=self.model_outputs[self.trig_name][0],
            mode="lines",
            name="sin",
        )

    def tab_click(self, **event_args):
        """This method is called when the button is clicked"""
        tab = event_args["sender"]
        for t in tab.parent.get_components():
            t.role = ""
        tab.role = "raised"
        self.trig_name = tab.text
        self.build_graphs()

    def tabs_show(self, **event_args):
        """This method is called when the FlowPanel is shown on the screen"""
        self.tab_1.role = "raised"
        self.trig_name = self.tab_1.text


