from ._anvil_designer import AmbitionLevelTemplate
from anvil import *
import anvil.server

class AmbitionLevel(AmbitionLevelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.slider.level = self.value

  def slider_1_change(self, level, **event_args):
    """This method is called when the slider is moved"""
    self.value_label.text = self.value = level
    self.raise_event("changed")

