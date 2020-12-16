from ._anvil_designer import AmbitionLeverTemplate
from anvil import *
import anvil.server

class AmbitionLever(AmbitionLeverTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run when the form opens.

#     if "name" not in self.item:
#         raise ValueError("Name must be provided for AmbitionLever")
    if "min" not in self.item:
        self.item['min'] = 0
    if "max" not in self.item:
        self.item['max'] = self.item.get('max', 4)
    if "step" not in self.item:
        self.item['step'] = 1
    self.update_value(self.item.get('value', 1))
    
    print(self.item)
        
    self.label.text = self.item.get('name',self.name)
    changed_handler = self.item.get('changed', None)
    if changed_handler is not None:
      self.set_event_handler("changed", changed_handler)
      
  def update_value(self, value):
    self.item['value'] = value
    self.slider.level = value
    self.value_label.text = value
    
  def slider_change(self, level, **event_args):
    """This method is called when the slider is moved"""
    self.update_value(level)
    self.raise_event("changed")
