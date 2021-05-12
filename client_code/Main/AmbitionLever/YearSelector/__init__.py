from ._anvil_designer import YearSelectorTemplate


class YearSelector(YearSelectorTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        year_list = list(map(str, range(2020, 2055, 5)))

        self.end_year.items = year_list
        self.start_year.items = year_list
        self.start_year.selected_value = "2020"
        self.end_year.selected_value = "2050"

        self.visible = False
