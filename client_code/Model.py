from collections import OrderedDict, namedtuple

import anvil.server

# This is a module.
# You can define variables and functions here, and use them from any form.


GraphInfo = namedtuple("GraphData", ("title", "output", "plot_type"))


def process_layout_data(data):
    """Take a json payload (`data`) of the weboutputs_summary_table named range and
    return a nested data structure of OrderedDict's such that:

    return_value[tab][sub_tab][position] = GraphInfo instance

    where:
    tab = string referencing an output tab
    sub_tab = string referencing an output sub-tab
    position = one of (1-5, "Top", "Bottom", "Page") indicating the position of
               an output within a sub-tab
    GraphInfo instance = The relevant metadata required to built an output
    """
    layout = OrderedDict()
    for tab, sub_tab, pos, title, named_ranges, plot_type in zip(
        data["Webtool Page"],
        data["Webtool Tab"],
        data["Position"],
        data["Title"],
        data["Named Range"],
        data["Graph Type"],
    ):

        # the following could be much neater with use of `setdefault` however,
        # at time of writing, the client environment for Anvil (based on
        # anvil-app-server==1.4) contains a bug which prevents its use
        if tab not in layout:
            layout[tab] = OrderedDict()
        sub_tabs = layout[tab]

        if sub_tab not in sub_tabs:
            sub_tabs[sub_tab] = OrderedDict()
        positions = sub_tabs[sub_tab]

        positions[pos] = GraphInfo(
            title,
            named_ranges.replace(".", "_").lower(),
            plot_type,
        )
    return layout


lever_groups = anvil.server.call("lever_groups")
layout = process_layout_data(anvil.server.call("layout"))
example_pathways = anvil.server.call("example_pathways")

language = "en"


# Use this to translate - later add a registration so all text can be translated at once
def translate(text):
    return anvil.server.call("translate", language, text)
