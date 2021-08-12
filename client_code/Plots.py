import anvil.server
import plotly.graph_objects as go

from .Model import init_vals


def _prepare_rows(data, x):
    """Retrieve the name and data for each trace in a plot.

    Args:
        data (list): The data to be plotted, includes names and values
        x (list): The x axis. A list of years.

    Yields:
        tuple: A (name, trace) tuple. Where name is a string and trace is a list.
    """
    for row in data[::-1]:
        name = row[0]
        trace = row[1 : len(x) + 1]
        yield name, trace


def _partial_scatter(x, y, name, **kwargs):
    return go.Scatter(x=x, y=y, name=name, showlegend=True, **kwargs)


def format_plot(plot, title):
    """Apply standard formatting to plot. For Anvil `Plot` objects this must be
    called before the `data` attribute of the plot is set.
    """
    layout = plot.layout
    layout.margin = dict(t=30, b=20, l=60, r=0)
    layout.hovermode = "closest"
    layout.title = dict(text=f"{title}", x=0.5)


def plot_stacked_area(plot, model_solution, output, title, axis_unit):
    """Plots the stacked area type of plots.
    The traces stack on top of each other to make a total.

    Args:
        plot (plotly.graph_objects.Figure): The figure in the anvil app
        model_solution (dict): The solution returned by the model
        output (str): The named range corresponding to the output for this plot
        title (str): The title of the figure
        axis_unit (str): Unit to add as y-axis title
    """
    format_plot(plot, title)
    plot.layout.yaxis.title = axis_unit
    model_output = model_solution[output]
    x = model_solution["x"]

    data = []
    total = None
    for name, y in _prepare_rows(model_output, x):
        if "total" in name.lower():
            total = _partial_scatter(
                x, y, name, mode="lines", line=dict(width=4, color="black")
            )
        elif all(val <= 0 for val in y):
            data.append(
                _partial_scatter(x, y, name=name, mode="lines", stackgroup="two")
            )
        else:
            data.append(
                _partial_scatter(x, y, name=name, mode="lines", stackgroup="one")
            )
    if total:
        data.append(total)
    plot.data = data


def plot_line(plot, model_solution, output, title, axis_unit):
    """Plots the line plot type of plots.
    The traces are plotted as individual line plots with markers.

    Args:
        plot (plotly.graph_objects.Figure): The figure in the anvil app
        model_solution (dict): The solution returned by the model
        output (str): The named range corresponding to the output for this plot
        title (str): The title of the figure
        axis_unit (str): Unit to add as y-axis title
    """
    format_plot(plot, title)
    plot.layout.yaxis.title = axis_unit
    model_output = model_solution[output]
    x = model_solution["x"]
    plot.data = [
        _partial_scatter(x, y, name, mode="lines+markers", marker=dict(symbol=num))
        for num, (name, y) in enumerate(_prepare_rows(model_output, x))
    ]


def plot_sankey(plot, model_solution, output, title, valuesuffix):
    """Creates and plots a Sankey flow diagram.

    Args:
        plot (plotly.graph_objects.Figure): The figure in the anvil app
        model_solution (dict): The solution returned by the model
        output (str): The named range corresponding to the output for this plot
        title (str): The title of the figure
        valuesuffice (str): Value passed as valuesuffix to Go.Sankey
    """
    format_plot(plot, title)
    data_index = model_solution["x"].index(init_vals["sankey_data_year"])
    model_output = model_solution[output]
    sources = []
    targets = []
    values = []
    for source, target, *data_row in model_output[1::]:
        sources.append(source)
        targets.append(target)
        values.append(data_row[data_index])
    nodes = list(set(sources + targets))
    sources = [nodes.index(source) for source in sources]
    targets = [nodes.index(target) for target in targets]

    plot.data = [
        go.Sankey(
            valueformat=".0f",
            valuesuffix=valuesuffix,
            node=dict(
                pad=15,
                thickness=15,
                line=dict(color="black", width=0.5),
                label=nodes,
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
            ),
        )
    ]


def plot_map(plot, model_solution, outputs, title, _=None):
    """Plot the Map type to show land areas over a map of the region.

    Args:
        plot (plotly.graph_objects.Figure): The figure in the anvil app
        model_solution (dict): The solution returned by the model
        outputs (str): The named ranges corresponding to the outputs for this plot
        title (str): The title of the figure
        _: dummy argument to match interface of other plotting routines
    """
    index = model_solution["x"].index(init_vals["maps_data_year"])
    data = {}
    for output in outputs.split(","):
        if "area" in output:
            key = "area"
        elif "distance" in output:
            key = "distance"
        else:
            continue
        data.setdefault(key, []).extend(
            [line[0], line[index]] for line in model_solution[output]
        )
    fig = anvil.server.call("map", data)
    format_plot(fig, title)
    plot.figure = fig


PLOTS_REGISTRY = {
    "stacked area with overlying line(s)": plot_stacked_area,
    "line": plot_line,
    "sankey/flow": plot_sankey,
    "map": plot_map,
}
"""Dictionary mapping plot type names to their functions."""
