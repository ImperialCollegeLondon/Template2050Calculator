from ._anvil_designer import YearSelectorTemplate


class YearSelector(YearSelectorTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        year_list = list(map(str, range(2020, 2105, 5)))

        self.end_year.items = year_list
        self.start_year.items = year_list
        self.start_year.selected_value = "2020"
        self.end_year.selected_value = "2050"

        self.visible = False

    def year_change(self, **event_args):
        """This method is called when the start or end year is changed"""
        ambition_lever = self.parent.parent
        ambition_lever.raise_event("x-refresh")
