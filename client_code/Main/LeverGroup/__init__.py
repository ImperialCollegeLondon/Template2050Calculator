from anvil import get_open_form

from ._anvil_designer import LeverGroupTemplate


class LeverGroup(LeverGroupTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        levers = self.item["levers"]
        inputs = self.item["inputs"]
        self.lever_panel.items = [
            dict(
                name=name,
                tooltips=tooltips,
                value=value,
                event_handler=self.lever_clicked,
            )
            for name, tooltips, value in zip(
                levers["names"], levers["tooltips"], inputs
            )
        ]

        group_value = sum(inputs) / len(inputs)
        self.group_lever.item = dict(
            name=self.item["name"],
            value=group_value,
            event_handler=self.group_lever_clicked,
        )

        self.lever_panel.visible = False

    def lever_clicked(self, **event_args):
        """`x-refresh` event handler used for ambition levers that are part of the
        group.
        """
        levers = self.lever_panel.get_components()
        mean_value = sum(lever.value for lever in levers) / len(levers)
        self.group_lever.value = mean_value
        # now update model based on new values
        main = get_open_form()
        main.update_graphs()

    def group_lever_clicked(self, **event_args):
        """`x-refresh` event handler for the group level ambition lever"""

        value = self.group_lever.value
        for lever in self.lever_panel.get_components():
            lever.value = value
        # now update model based on new values
        main = get_open_form()
        main.update_graphs()

    def arrow_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.lever_panel.visible = not self.lever_panel.visible
        if self.lever_panel.visible:
            self.arrow_button.icon = "fa:angle-down"
        else:
            self.arrow_button.icon = "fa:angle-right"
