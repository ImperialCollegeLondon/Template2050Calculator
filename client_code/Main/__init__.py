from anvil import get_url_hash, set_url_hash

from .. import Model
from ._anvil_designer import MainTemplate
from .FiguresPanel import FiguresPanel

# Uncomment for Thai language
# Model.language = "th"


class Main(MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.

        self.set_ambition_levers()
        self.pathways_dropdown.items = Model.example_pathways.keys()

        self.select_figures()
        self.update_graphs()

        self.title.text = Model.translate("2050 Carbon Calculator")
        self.expert_label.visible = False

    def select_figures(self):
        self.figures_panel = FiguresPanel()
        self.plot_area.clear()
        self.plot_area.add_component(self.figures_panel)

    def update_graphs(self):
        """Collect the level values and update the graphs and url hash."""
        inputs = [
            (lever.value, lever.start_year, lever.end_year)
            for group in self.lever_group_panel.get_components()
            for lever in group.lever_panel.get_components()
        ]
        self.set_url(*zip(*inputs))
        self.figures_panel.calculate(*zip(*inputs))

    def get_url_vals(self):
        """Get lever values from url, if available. Otherwise use defaults."""
        url_hash = get_url_hash()
        if url_hash:
            return dict(
                inputs=list(map(float, url_hash["inputs"].split("-"))),
                start_years=list(map(int, url_hash["start_years"].split("-"))),
                end_years=list(map(int, url_hash["end_years"].split("-"))),
            )
        else:
            inputs = Model.default_inputs.copy()
            start_years = Model.default_start_years.copy()
            end_years = Model.default_end_years.copy()
            self.set_url(inputs, start_years, end_years)
            return dict(inputs=inputs, start_years=start_years, end_years=end_years)

    def set_url(self, inputs, start_years, end_years):
        """Set lever values in the url.

        Args:
            inputs (list): A list of lever values
        """
        set_url_hash(
            dict(
                inputs="-".join(map(str, inputs)),
                start_years="-".join(map(str, start_years)),
                end_years="-".join(map(str, end_years)),
            )
        )

    def set_ambition_levers(self):
        input_values = self.get_url_vals()
        self.lever_group_panel.items = [
            {
                "name": name,
                "levers": levers,
                "inputs": [
                    input_values["inputs"].pop(0) for _ in range(len(levers["names"]))
                ],
                "start_years": [
                    input_values["start_years"].pop(0)
                    for _ in range(len(levers["names"]))
                ],
                "end_years": [
                    input_values["end_years"].pop(0)
                    for _ in range(len(levers["names"]))
                ],
            }
            for name, levers in Model.lever_groups.items()
        ]

    def pathways_dropdown_change(self, **event_args):
        """This method is called when an item is selected from the dropdown"""
        self.set_url(
            Model.example_pathways[event_args["sender"].selected_value],
            Model.default_start_years.copy(),
            Model.default_end_years.copy(),
        )
        self.set_ambition_levers()
        self.update_graphs()

    def reset_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.pathways_dropdown.selected_value = None
        self.set_url(
            Model.default_inputs.copy(),
            Model.default_start_years.copy(),
            Model.default_end_years.copy(),
        )
        self.set_ambition_levers()
        self.update_graphs()

    def expert_toggle_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.expert_label.visible = not self.expert_label.visible
        for group in self.lever_group_panel.get_components():
            for lever in group.lever_panel.get_components():
                lever.years.visible = self.expert_label.visible
