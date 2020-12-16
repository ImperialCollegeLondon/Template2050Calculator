from ._anvil_designer import AmbitionLeverTemplate
from anvil import *
import anvil.server

class AmbitionLever(AmbitionLeverTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.
    self.slider.slider_min = self.item.get('min', 1)
    self.slider.slider_max = self.item.get('max', 4)
    self.slider.step = self.item.get('step', 1)
    self.update_value(self.item.get('value', 1))
    
    self.label.text = self.item.get('name', "NoName")

  def update_value(self, value):
    self.item['value'] = value
    self.slider.level = value
    self.value_label.text = value
    
  def slider_change(self, level, **event_args):
    """This method is called when the slider is moved"""
    self.update_value(level)
    self.parent.raise_event("x-refresh")
