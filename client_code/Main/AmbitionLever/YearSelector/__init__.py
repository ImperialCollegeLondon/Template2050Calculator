from ....Model import init_vals
from ._anvil_designer import YearSelectorTemplate


class YearSelector(YearSelectorTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        year_range = init_vals["expert_mode_range"]
        self._year_step = year_range["step_size"]
        year_list = [
            (str(val), val)
            for val in range(
                year_range["min_year"],
                year_range["max_year"] + year_range["step_size"],
                year_range["step_size"],
            )
        ]

        self.start_year.items = year_list[:-1]
        self.end_year.items = year_list[1:]

    def year_change(self, **event_args):
        """This method is called when the start or end year is changed"""

        if self.start_year.selected_value >= self.end_year.selected_value:
            if event_args["sender"] is self.start_year:
                self.end_year.selected_value = (
                    self.start_year.selected_value + self._year_step
                )
            elif event_args["sender"] is self.end_year:
                self.start_year.selected_value = (
                    self.end_year.selected_value - self._year_step
                )

        ambition_lever = self.parent.parent
        ambition_lever.raise_event("x-refresh")
