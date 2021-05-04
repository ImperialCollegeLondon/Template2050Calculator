from ._anvil_designer import LeverGroupTemplate


class LeverGroup(LeverGroupTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        levers = self.item["levers"]
        inputs = self.item["inputs"]
        self.lever_panel.items = [
            {"name": name, "tooltips": tooltips, "value": value}
            for name, tooltips, value in zip(
                levers["names"], levers["tooltips"], inputs
            )
        ]

        group_value = round(sum(inputs) / len(inputs), 1)
        self.group_lever.item = {"name": self.item["name"], "value": group_value}

        self.lever_panel.visible = False
        self.set_event_handler("x-refresh", self.group_lever_clicked)

    def lever_clicked(self, **event_args):
        """`x-refresh` event handler for the repeating panel containing individual
        ambition levers.
        """
        levers = self.lever_panel.get_components()
        average = round(
            sum([int(lever.item["value"]) for lever in levers]) / len(levers), 1
        )
        self.group_lever.update_value(average)
        # now update model based on new values
        self.parent.raise_event("x-refresh")

    def group_lever_clicked(self, **event_args):
        """`x-refresh` event handler for this object"""
        value = self.group_lever.item["value"]
        for lever in self.lever_panel.get_components():
            lever.update_value(value)
        self.parent.raise_event("x-refresh")

    def arrow_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.lever_panel.visible = not self.lever_panel.visible
        if self.lever_panel.visible:
            self.arrow_button.icon = "fa:angle-down"
        else:
            self.arrow_button.icon = "fa:angle-right"

    def show_lever(self, **event_args):
        """The `show` event handler for self.group_lever"""
        event_args["sender"].complete_init()
