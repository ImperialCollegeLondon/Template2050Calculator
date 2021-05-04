from ._anvil_designer import AmbitionLeverTemplate


class AmbitionLever(AmbitionLeverTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # if init'd outside of a repeating panel self.item will not yet be set
        try:
            self.complete_init()
        except KeyError:
            pass

    def complete_init(self):
        """Set lever properties from self.item. __init__ attempts to call this method
        however if self.item has not yet been set it should be called when the
        object's `show` event is triggered.
        """

        self.update_value(self.item["value"])

        self.label.text = self.item["name"]
        tooltips = self.item.get("tooltips", [""] * 5)
        self.label.tooltip = tooltips[0]
        for i, (level, tip) in enumerate(zip(self.slider.levels, tooltips[1:]), 1):
            level.tooltip = f"Ambition Level {i}:\n" + tip

    def update_value(self, value):
        self.item["value"] = value
        self.slider.level = value

    def lever_change(self, level, **event_args):
        """This method is called when lever level is changed"""
        self.update_value(level)
        self.parent.raise_event("x-refresh")
