from collections import OrderedDict, namedtuple

import anvil.server

# This is a module.
# You can define variables and functions here, and use them from any form.


GraphInfo = namedtuple("GraphData", ("title", "output", "plot_type", "axis_unit"))


def process_layout_data(data):
    """Take a json payload (`data`) of the weboutputs_summary_table named range and
    return a nested data structure of OrderedDict's such that:

    return_value[tab][sub_tab][position] = GraphInfo instance

    where:
        - tab = string referencing an output tab
        - sub_tab = string referencing an output sub-tab
        - position = one of (1-5, "Top", "Bottom", "Page") indicating the position of
          an output within a sub-tab
        - GraphInfo instance = The relevant metadata required to built an output

    Returns:
        OrderedDict: Structured data of the layout of the figures in the web app.
    """
    layout = OrderedDict()
    for tab, sub_tab, pos, title, named_ranges, plot_type, axis_unit in zip(
        data["Webtool Page"],
        data["Webtool Tab"],
        data["Position"],
        data["Title"],
        data["Named Range"],
        data["Graph Type"],
        data["Axis Unit"],
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
            title, named_ranges.replace(".", "_").lower(), plot_type, axis_unit
        )
    return layout


init_vals = anvil.server.call("initial_values")
if "layout" in init_vals.keys():
    init_vals["layout"] = process_layout_data(init_vals["layout"])

language = "en"
"""The language for the web app. The `locale` in
:meth:`server_code.Model2050Server.translate`. Set to "th" for Thai language example.
"""


# Use this to translate - later add a registration so all text can be translated at once
def translate(text):
    """Translate the text into the already selected language. Calls server function
    :meth:`server_code.Model2050Server.translate`.

    Args:
        text (str): The text to be translated.

    Returns:
        str: The translated text.
    """
    return anvil.server.call("translate", language, text)
