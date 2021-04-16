from ._anvil_designer import FiguresPanelTemplate
from anvil import *
import anvil.server
import plotly.graph_objects as go

from ... import Model


class FiguresPanel(FiguresPanelTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.build_tabs()

        self.card_1.add_component(Label(text=anvil.server.call("web_outputs_keys")))

    def build_tabs(self):
        for i, output in enumerate(Model.outputs):
            if output in ("x", "warning_l4chosen", "lever_names"):
                continue
            tab = Button(text=f"{output.title()} Plot")
            tab.tag = output
            tab.set_event_handler("click", self.tab_click)
            self.tabs.add_component(tab)
            if i == 0:
                self.selected_tab = tab

    def calculate(self, inputs):
        self.model_solution = anvil.server.call("calculate", list(inputs.values()))
        self.build_graphs()
        self.update_warnings()

    def update_warnings(self):
        l4_status = self.model_solution["warning_l4chosen"][0][1]
        if l4_status == 0:
            self.l4_warning.icon = "fa:square-o"
        elif l4_status == 1:
            self.l4_warning.icon = "fa:check-square"
        else:
            self.l4_warning.icon = "fa:asterisk"

    def build_graphs(self):
        output = self.selected_tab.tag
        self.plot.layout.title = f"{output.title()} Graph"
        self.plot.layout.margin.t = 30
        self.plot.layout.margin.b = 20
        self.plot.layout.margin.l = 30
        self.plot.layout.margin.r = 10
        self.plot.layout.hovermode = "closest"
        x = self.model_solution["x"]
        self.plot.data = [
            go.Scatter(
                x=x,
                y=y,
                mode="lines",
                stackgroup="one",
                name=name,
                showlegend=True,
            )
            for name, y in _prepare_rows(self.model_solution[output], x)
        ]

    @property
    def selected_tab(self):
        return self._selected_tab

    @selected_tab.setter
    def selected_tab(self, tab):
        for t in self.tabs.get_components():
            t.role = "raised" if t is tab else ""
        self._selected_tab = tab

    def tab_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.selected_tab = event_args["sender"]
        self.build_graphs()


def _prepare_rows(data, x):
    for row in data[::-1]:
        name = row[0]
        trace = row[1: len(x) + 1]
        yield name, trace
