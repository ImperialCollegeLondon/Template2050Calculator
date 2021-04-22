from ._anvil_designer import AmbitionLeverTemplate
from anvil import *
import anvil.server


class AmbitionLever(AmbitionLeverTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.update_value(self.item["value"])

        self.label.text = self.item.get("name", "NoName")

    def update_value(self, value):
        self.item["value"] = value
        self.slider.level = value

    def lever_change(self, level, **event_args):
        """This method is called when lever level is moved"""
        self.update_value(level)
        self.parent.raise_event("x-refresh")
