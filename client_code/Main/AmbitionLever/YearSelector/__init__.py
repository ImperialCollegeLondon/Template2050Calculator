from ._anvil_designer import YearSelectorTemplate


class YearSelector(YearSelectorTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        self.start_year.slider_min = 2020
        self.end_year.slider_min = 2020
        self.start_year.slider_max = 2105
        self.end_year.slider_max = 2105

        self.end_year.step = 5
        self.start_year.step = 5

        self.visible = False
        
    def update_text(self):
        self.start_label.text = str(self.start_year.level)
        self.end_label.text = str(self.end_year.level)

    def year_change(self, **event_args):
        """This method is called when the start or end year is changed"""
        
        self.update_text()

        ambition_lever = self.parent.parent
        ambition_lever.raise_event("x-refresh")

    def form_show(self, **event_args):
      """This method is called when the column panel is shown on the screen"""
      self.update_text()
