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

    def complete_init(
        self,
        name,
        value,
        event_handler,
        start_year=None,
        end_year=None,
        tooltips=[""] * 5,
        bold=False,
    ):
        """Set lever properties"""

        self.value = value
        self.start_year = start_year
        self.end_year = end_year

        self.label.text = name
        self.label.bold = bold
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

    @property
    def start_year(self):
        return int(self.years.start_year.level)

    @start_year.setter
    def start_year(self, start_year):
        self.years.start_year.level = str(start_year)

    @property
    def end_year(self):
        return int(self.years.end_year.level)

    @end_year.setter
    def end_year(self, end_year):
        self.years.end_year.level = str(end_year)
