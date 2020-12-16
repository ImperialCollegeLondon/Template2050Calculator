from ._anvil_designer import AmbitionLevelsTemplate
from anvil import *
import anvil.server

class AmbitionLevels(AmbitionLevelsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
#     self._value = properties["value"]


    # Any code you write here will run when the form opens.
#     self.slider.level = self.value
    print(properties)
    print(f"self.item = {self.item} - {self.name}")
    self.label.text = self.item.get('name',self.name)
    changed_handler = self.item.get('changed', None)
    print(changed_handler)
    if changed_handler is not None:
      self.set_event_handler("changed", changed_handler)
    
    
  def slider_change(self, level, **event_args):
    """This method is called when the slider is moved"""
    #self.value_label.text = 
    self.value = level
    self.raise_event("changed")

  @property
  def value(self):
    return self._value
  
  @value.setter
  def value(self, value):
    self._value = value
