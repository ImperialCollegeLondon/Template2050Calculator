from ._anvil_designer import AmbitionLeverTemplate


class AmbitionLever(AmbitionLeverTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.update_value(self.item["value"])

        self.label.text = self.item.get("name", "NoName")
        tooltips = self.item.get("tooltips", "")
        self.label.tooltip = tooltips[0]
        for level, tip in zip(self.slider.levels, tooltips[1:]):
            level.tooltip = tip

    def update_value(self, value):
        self.item["value"] = value
        self.slider.level = value

    def slider_change(self, level, **event_args):
        """This method is called when the slider is moved"""
        self.update_value(level)
        self.parent.raise_event("x-refresh")
