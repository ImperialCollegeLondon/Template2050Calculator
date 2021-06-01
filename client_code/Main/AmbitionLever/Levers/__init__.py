from ._anvil_designer import LeversTemplate


class Levers(LeversTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.levels = [self.level_1, self.level_2, self.level_3, self.level_4]

    def level_click(self, **event_args):
        """This method is called when the lever is clicked"""
        button_index = self.levels.index(event_args["sender"])
        if button_index < self.level <= button_index + 1:
            self.level -= 0.1
        else:
            self.level = button_index + 1
        ambition_lever = self.parent.parent
        ambition_lever.raise_event("x-refresh")

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = round(level, 1)
        self._level = 1.0 if self._level < 1.0 else self._level
        self._level = 4.0 if self._level > 4.0 else self._level

        for i, level_button in enumerate(self.levels, 1):
            if i < self._level:
                level_button.background = "theme:Black"
                level_button.foreground = "theme:Black"
            elif i == self._level:
                level_button.background = "theme:Black"
                level_button.foreground = "theme:White"
                level_button.text = f"{int(i):d}"
            elif i - 1 < self._level < i:
                decimal = int(10 * (self._level - i + 1))
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
