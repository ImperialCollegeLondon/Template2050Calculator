import anvil.server
import plotly.graph_objects as go


def _prepare_rows(data, x):
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
    layout.margin = dict(t=30, b=20, l=30, r=10)
    layout.hovermode = "closest"
    layout.title = dict(text=f"{title}", x=0.5)


def plot_stacked_area(plot, model_solution, output, title):
    format_plot(plot, title)
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


def plot_line(plot, model_solution, output, title):
    format_plot(plot, title)
    model_output = model_solution[output]
    x = model_solution["x"]
    plot.data = [
        _partial_scatter(x, y, name, mode="lines+markers", marker=dict(symbol=num))
        for num, (name, y) in enumerate(_prepare_rows(model_output, x))
    ]


def plot_sankey(plot, model_solution, output, title):
    format_plot(plot, title)
    x = model_solution["x"]
    model_output = model_solution[output]
    sources = []
    targets = []
    values = []
    for row in model_output[1::]:
        sources.append(row[0])
        targets.append(row[1])
        values.append(row[len(x) + 1])

    nodes = list(set(sources + targets))
    sources = [nodes.index(source) for source in sources]
    targets = [nodes.index(target) for target in targets]

    plot.data = [
        go.Sankey(
            valueformat=".0f",
            valuesuffix="TWh",  # Get from Model2050Server.TABLE["Axis Unit"] ?
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


def plot_map(plot, model_solution, outputs, title):
    # 2050 should be a configurable parameter
    index = model_solution["x"].index(2050)
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
