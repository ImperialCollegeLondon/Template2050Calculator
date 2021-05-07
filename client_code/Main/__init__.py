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

    def get_lever_vals(self):
        """Get lever values from url, if available. Otherwise use defaults."""
        url_hash = get_url_hash()
        return (
            (
                tuple(map(float, input_str.split(",")))
                for input_str in url_hash.split(";")
            )
            if url_hash
            else ((val, 2020, 2050) for val in Model.inputs)
        )

    def set_url(self, inputs, start_years=None, end_years=None):
        """Set lever values in the url.

        Args:
            inputs (list): A list of lever values
        """
        if start_years and end_years:
            set_url_hash(
                ";".join(
                    [
                        f"{val},{start},{end}"
                        for val, start, end in zip(inputs, start_years, end_years)
                    ]
                )
            )
        else:
            set_url_hash(";".join([f"{val},{2020},{2050}" for val in inputs]))

    def set_ambition_levers(self):
        input_values = list(self.get_lever_vals())
        self.lever_group_panel.items = [
            {
                "name": name,
                "levers": levers,
                "inputs": [input_values.pop(0)[0] for _ in range(len(levers["names"]))],
            }
            for name, levers in Model.lever_groups.items()
        ]

    def pathways_dropdown_change(self, **event_args):
        """This method is called when an item is selected from the dropdown"""
        self.set_url(Model.example_pathways[event_args["sender"].selected_value])
        self.set_ambition_levers()
        self.update_graphs()

    def reset_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.pathways_dropdown.selected_value = None
        self.set_url(Model.inputs)
        self.set_ambition_levers()
        self.update_graphs()
