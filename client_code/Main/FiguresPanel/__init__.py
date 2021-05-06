import anvil.server
from anvil import Button, Label, Plot

from ... import Model
from ...Plots import PLOTS_REGISTRY
from ._anvil_designer import FiguresPanelTemplate


class FiguresPanel(FiguresPanelTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.build_tabs()

    def build_tabs(self):
        layout = Model.layout

        tabs = [
            self._add_button(self.tabs, tab)
            for tab in layout.keys()
            if tab.lower() not in ("warnings", "key indicators")
        ]
        sub_tab = self.build_sub_tabs(tabs[0])
        self.selected_tab = tabs[0], sub_tab

    def build_sub_tabs(self, tab):
        self.sub_tabs.clear()
        layout = Model.layout
        sub_tabs = [
            self._add_button(self.sub_tabs, sub_tab) for sub_tab in layout[tab.tag]
        ]
        return sub_tabs[0]

    def _add_button(self, element, name):
        button = Button(text=name)
        button.tag = name
        button.set_event_handler("click", self.tab_click)
        element.add_component(button)
        return button

    def calculate(self, inputs):
        self.model_solution = anvil.server.call("calculate", list(inputs))
        self.build_graphs()
        self.build_warnings()

    def build_warnings(self):
        self.warnings_panel.clear()
        warnings = Model.layout["Warnings"]["Not required"]

        for key in warnings:
            name, output, plot_type = warnings[key]
            data = self.model_solution[output]
            active = data[0][1]
            tooltip = data[1][1]

            label = Label()
            if active:
                label.icon = "fa:check-square"
            else:
                label.icon = "fa:square-o"
            self.warnings_panel.add_component(label)
            label.text = name
            label.tooltip = tooltip

    def build_graphs(self):
        self.figure_container.clear()
        layout = Model.layout
        tab, sub_tab = self.selected_tab
        try:
            self._plot(layout[tab.tag][sub_tab.tag]["Top"])
            self._plot(layout[tab.tag][sub_tab.tag]["Bottom"])
        except KeyError:
            try:
                self._plot(layout[tab.tag][sub_tab.tag]["Page"])
            except KeyError:
                pass

    def _plot(self, graph_data):
        plot = Plot()
        self.figure_container.add_component(plot)
        title, output, plot_type = graph_data
        PLOTS_REGISTRY[plot_type.lower()](plot, self.model_solution, output, title)

    @property
    def selected_tab(self):
        return self._selected_tab

    @selected_tab.setter
    def selected_tab(self, tab):
        for t in self.tabs.get_components():
            t.role = "raised" if t is tab[0] else ""
        for t in self.sub_tabs.get_components():
            t.role = "raised" if t is tab[1] else ""
        self._selected_tab = tab

    def tab_click(self, **event_args):
        """This method is called when the button is clicked"""
        current_tab, current_sub_tab = self.selected_tab
        sender = event_args["sender"]
        if sender in self.tabs.get_components():
            current_tab = sender
            current_sub_tab = self.build_sub_tabs(current_tab)
        elif sender in self.sub_tabs.get_components():
            current_sub_tab = sender
        self.selected_tab = current_tab, current_sub_tab

        self.build_graphs()
