from anvil import get_open_form

from ._anvil_designer import LeverGroupTemplate


class LeverGroup(LeverGroupTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        levers = self.item["levers"]
        inputs = self.item["inputs"]
        start_years = self.item["start_years"]
        end_years = self.item["end_years"]
        self.lever_panel.items = [
            dict(
                name=name,
                tooltips=tooltips,
                value=value,
                event_handler=self.lever_clicked,
                start_year=start_year,
                end_year=end_year,
            )
            for name, tooltips, value, start_year, end_year in zip(
                levers["names"], levers["tooltips"], inputs, start_years, end_years
            )
        ]

        group_value = sum(inputs) / len(inputs)
        self.group_lever.item = dict(
            name=self.item["name"],
            value=group_value,
            event_handler=self.group_lever_clicked,
            bold=True,
            click_event_handler=self.arrow_button_click,
        )

        self.lever_panel.visible = False
        self.lever_spacer.visible = False
        self.set_event_handler("show", self.show)

    def show(self, **event_args):
        """`show` event handler. Control for any out of range input values that will
        have been changed.
        """

        self.lever_updated()

    def lever_updated(self):
        """Update the group lever value when one of the sub-levers is changed."""
        levers = self.lever_panel.get_components()
        mean_value = sum(lever.value for lever in levers) / len(levers)
        self.group_lever.value = mean_value

    def lever_clicked(self, **event_args):
        """`x-refresh` event handler used for ambition levers that are part of the
        group.
        """
        self.lever_updated()
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
        self.lever_spacer.visible = not self.lever_spacer.visible
        if self.lever_panel.visible:
            self.arrow_button.icon = "fa:angle-down"
        else:
            self.arrow_button.icon = "fa:angle-right"
