from ._anvil_designer import AmbitionLeverTemplate


class AmbitionLever(AmbitionLeverTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.set_event_handler("show", self.show)

    def show(self, **event_args):
        """`show` event handler. Expects self.item to be populated with required
        data for arguments of `complete_init`.
        """

        self.complete_init(**self.item)

    def complete_init(self, name, value, event_handler, tooltips=[""] * 5):
        """Set lever properties"""

        self.value = value

        self.label.text = name
        self.label.tooltip = tooltips[0]
        for i, (level, tip) in enumerate(zip(self.slider.levels, tooltips[1:]), 1):
            level.tooltip = f"Ambition Level {i}:\n" + tip
        self.set_event_handler("x-refresh", event_handler)

    @property
    def value(self):
        return self.slider.level

    @value.setter
    def value(self, value):
        self.slider.level = value
