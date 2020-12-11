from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go

class Form1(Form1Template):

  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.build_revenue_graph()
  
  def build_revenue_graph(self):
    self.plot_1.data = go.Bar(y=[100,400,200,300,500])

