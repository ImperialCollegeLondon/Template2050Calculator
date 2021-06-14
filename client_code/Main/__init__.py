from anvil import Label, get_url_hash, set_url_hash

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

        self.set_event_handler("show", self.show)

    def show(self, **event_args):
        """`show` event handler. Last function to be called."""
        self.expert_label = Label(text="Start and End Year")
        self.expert_toggle.text = "Switch to 2100 Mode"
        self.select_figures()
        self.update_graphs()

        self.title.text = Model.translate("2050 Carbon Calculator")

    def select_figures(self):
        """Initialise the FiguresPanel and add it to the plot area of the app."""
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
        self.figures_panel.calculate(*zip(*inputs), expert_mode=self.expert_mode)

    def get_url_vals(self):
        """Get lever values from url, if available. Otherwise use defaults."""
        url_hash = get_url_hash()
        if not url_hash:
            self.set_defaults()
            url_hash = get_url_hash()
        return dict(
            inputs=list(map(float, url_hash["inputs"].split("-"))),
            start_years=list(map(int, url_hash["start_years"].split("-"))),
            end_years=list(map(int, url_hash["end_years"].split("-"))),
        )

    def set_url(self, inputs=None, start_years=None, end_years=None):
        """Set lever values in the url.

        Args:
            inputs (list): A list of lever values
        """
        url_hash = get_url_hash()
        if inputs is None:
            inputs = url_hash["inputs"]
        else:
            inputs = "-".join(map(str, inputs))

        if start_years is None or end_years is None:
            start_years = url_hash["start_years"]
            end_years = url_hash["end_years"]
        else:
            start_years = "-".join(map(str, start_years))
            end_years = "-".join(map(str, end_years))

        set_url_hash(dict(inputs=inputs, start_years=start_years, end_years=end_years))

    def set_defaults(self, years_only=False):
        """Set the url values (for levers and years) to their defaults.

        Args:
            years_only (bool): True when only changing the start and end year values and
                leaving the lever values. False also sets levers to defaults.
        """
        if years_only:
            self.set_url(
                start_years=Model.default_start_years.copy(),
                end_years=Model.default_end_years.copy(),
            )
        else:
            self.set_url(
                Model.default_inputs.copy(),
                Model.default_start_years.copy(),
                Model.default_end_years.copy(),
            )

    def set_ambition_levers(self):
        """Set the values of the AmbitionLevers to match the urls.

        Updates the values if the LeverGroup is already populated, otherwise populates
        the LeverGroup.
        """
        input_values = self.get_url_vals()
        if self.lever_group_panel.items is None:
            self.lever_group_panel.items = [
                {
                    "name": name,
                    "levers": levers,
                    "inputs": [
                        input_values["inputs"].pop(0)
                        for _ in range(len(levers["names"]))
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
        else:
            for group in self.lever_group_panel.get_components():
                for lever in group.lever_panel.get_components():
                    lever.value = input_values["inputs"].pop(0)
                    lever.start_year = input_values["start_years"].pop(0)
                    lever.end_year = input_values["end_years"].pop(0)
                group.lever_updated()

    def pathways_dropdown_change(self, **event_args):
        """This method is called when an item is selected from the dropdown"""
        self.set_defaults(years_only=True)
        self.set_url(Model.example_pathways[event_args["sender"].selected_value])
        self.set_ambition_levers()
        self.update_graphs()

    def reset_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.pathways_dropdown.selected_value = None
        self.set_defaults()
        self.set_ambition_levers()
        self.update_graphs()

    @property
    def expert_mode(self):
        """A boolean property of the current app mode. True if in Expert Mode."""
        return self.expert_label in self.settings_title_card.get_components()

    def expert_toggle_click(self, **event_args):
        """This method is called when the `expert_toggle` button is clicked."""
        self.set_expert_mode(not self.expert_mode)
        self.update_graphs()

    def set_expert_mode(self, expert_mode):
        """Change app mode into Expert or back to Standard Mode.

        Expert Mode gives the option to select the start and end years for each Ambition
        Lever and extends the graphs into 2100. Standard Mode resets start and end year
        values to defaults and removes the ability to edit them and returns the year max
        to 2050.

        Args:
            expert_mode (bool): True when converting the app into Expert Mode.
        """
        if expert_mode:
            self.expert_toggle.text = "Go back to 2050 Mode"
            self.settings_title_card.add_component(self.expert_label)
        else:
            self.expert_toggle.text = "Switch to 2100 Mode"
            self.expert_label.remove_from_parent()
            self.set_defaults(years_only=True)
            self.set_ambition_levers()

        for group in self.lever_group_panel.get_components():
            if not expert_mode:
                # Reset lever_panel to return to original (non-expert) layout.
                # lever_panel.items only includes the label and lever buttons, assigning
                # it re-initialises the levers in the panel.
                group.lever_panel.items = group.lever_panel.items
                continue
            for lever in group.lever_panel.get_components():
                lever.show_years()
