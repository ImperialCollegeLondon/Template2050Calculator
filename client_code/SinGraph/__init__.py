from ._anvil_designer import SinGraphTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go

class SinGraph(SinGraphTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
  
  def build_sin_graph(self):
    anvil.server.call("say_hello", self.period_input.text)
    self.sin_plot.data = go.Scatter(
      x=[1,2,3,4,5],
      y=[100,400,200,300,500],
      mode='lines',
      name='lines',
    )
    self.sin_plot.layout.title = (
      "Sin Graph with period = " +
      self.period_input.text + 
      " and phase = " +
      self.phase_input.text
    )

  def build_graph_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.build_sin_graph()

  def period_input_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.build_sin_graph()

  def phase_input_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.build_sin_graph()



