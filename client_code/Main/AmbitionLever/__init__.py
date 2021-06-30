from ._anvil_designer import AmbitionLeverTemplate
from .YearSelector import YearSelector


class AmbitionLever(AmbitionLeverTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.set_event_handler("show", self.show)
        self.years = YearSelector()

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
        start_year=2020,
        end_year=2050,
        tooltips=[""] * 5,
        bold=False,
        click_event_handler=None,
    ):
        """Set lever properties"""

        if not click_event_handler:
            click_event_handler = self.show_info

        self.value = value
        self.start_year = start_year
        self.end_year = end_year

        self.label.text = name
        self.label.bold = bold
        self.label.tooltip = tooltips[0]
        for i, (level, tip) in enumerate(zip(self.lever.levels, tooltips[1:]), 1):
            level.tooltip = f"Ambition Level {i}:\n" + tip
        self.set_event_handler("x-refresh", event_handler)
        self.label.set_event_handler("click", click_event_handler)

    def show_years(self):
        self.panel.add_component(self.years)

    @property
    def value(self):
        self.item["value"] = self.lever.level
        return self.lever.level

    @value.setter
    def value(self, value):
        self.lever.level = value

    @property
    def start_year(self):
        return self.years.start_year.selected_value

    @start_year.setter
    def start_year(self, start_year):
        self.years.start_year.selected_value = self._take_closest(
            start_year, self.years.start_year.items
        )

    @property
    def end_year(self):
        return self.years.end_year.selected_value

    @end_year.setter
    def end_year(self, end_year):
        self.years.end_year.selected_value = self._take_closest(
            end_year, self.years.end_year.items
        )

    def show_info(self, **event_kwargs):
        """Display a popup showing collected tooltip information for the lever"""
        from anvil import alert

        title = self.label.text
        content = (
            self.label.tooltip
            + "\n\n"
            + "\n\n".join(lever.tooltip for lever in self.lever.levels)
        )
        alert(title=title, content=content, large=True)

    def _take_closest(self, year, items):
        """Take the closest valid year value from items."""
        valid_years = [item[1] for item in items]
        if year not in valid_years:
            year = min(valid_years, key=lambda x: abs(x - year))
        return year
