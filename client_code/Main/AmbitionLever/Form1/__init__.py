from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run when the form opens.
    self.levels = [self.level_1, self.level_2, self.level_3, self.level_4]

  def level_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.parent.parent.slider_change(int(event_args['sender'].text))
    
  @property
  def level(self):
    return self._level
  
  @level.setter
  def level(self, level):
    self._level = level
    colour = "theme:Black"
    for i, level_button in enumerate(self.levels,1):
      if i > level:
        colour = "theme:White"
      level_button.background = colour
      level_button.foreground = colour

