from ._anvil_designer import YearSelectorTemplate
from anvil import *
import anvil.server

class YearSelector(YearSelectorTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.set_event_handler("show", self.show)
        self.set_event_handler("hide", self.hide)

        
    def show(self, start, end, year_list):
        self.end_year.items = year_list
        self.start_year.items = year_list
        
        self.start_year.selected_value = start
        self.end_year.selected_value = end
