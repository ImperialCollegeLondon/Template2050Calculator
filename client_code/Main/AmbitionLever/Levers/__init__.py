from ._anvil_designer import LeversTemplate


class Levers(LeversTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.levels = [self.level_1, self.level_2, self.level_3, self.level_4]

    def level_click(self, **event_args):
        """This method is called when the lever is clicked"""
        new_level = float(event_args["sender"].text)
        # Decrese level by 0.1 if already selected button is clicked
        if self.level == new_level and self.level != 1:
            new_level = round(new_level - 0.1, 1)
        # Ensure button is original integer value when clicked anew
        elif new_level != int(new_level):
            new_level = int(new_level) + 1
        self.parent.parent.lever_change(new_level)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        for i, level_button in enumerate(self.levels, 1):
            if i < level:
                level_button.background = "theme:Black"
                level_button.foreground = "theme:Black"
            elif i == level:
                level_button.text = level
                level_button.background = "theme:Black"
                level_button.foreground = "theme:White"
                level_button.text = f"{int(level):d}"
            elif i - 1 < level < i:
                level_button.text = level
                decimal = int(10 * round(level - i + 1, 1))
                level_button.background = "theme:Gray " + str(decimal) + "00"
                level_button.text = f"{level:.1f}"
                # change button text colour depending on shade of gray
                if decimal <= 5:
                    level_button.foreground = "theme:Black"
                else:
                    level_button.foreground = "theme:White"
            else:
                level_button.foreground = "theme:White"
                level_button.background = "theme:White"
