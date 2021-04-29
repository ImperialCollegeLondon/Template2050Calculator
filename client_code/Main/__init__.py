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

        self.ambition_levers.items = [
            {
                "name": name,
                "value": value,
                "tooltips": descriptions,
            }
            for name, value, descriptions in zip(
                Model.levers, self.get_lever_vals(), Model.lever_descriptions
            )
        ]

        self.ambition_levers.set_event_handler("x-refresh", self.update_graphs)
        self.select_figures()
        self.update_graphs()

        self.title.text = Model.translate("2050 Carbon Calculator")

    def select_figures(self):
        self.figures_panel = FiguresPanel()
        self.plot_area.clear()
        self.plot_area.add_component(self.figures_panel)

    def update_graphs(self, **event_args):
        """Collect the lever values and update the graphs and url hash."""
        inputs = {item["name"]: item["value"] for item in self.ambition_levers.items}
        self.set_url(inputs)
        self.figures_panel.calculate(inputs)

    def get_lever_vals(self):
        """Get lever values from url, if available. Otherwise use defaults."""
        url_hash = get_url_hash()
        return map(float, url_hash.split(",")) if url_hash else Model.inputs

    def set_url(self, inputs):
        """Set lever values in the url."""
        set_url_hash(",".join([str(val) for val in inputs.values()]))
