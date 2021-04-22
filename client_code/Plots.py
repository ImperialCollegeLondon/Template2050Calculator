import plotly.graph_objects as go


def _prepare_rows(data, x):
    for row in data[::-1]:
        name = row[0]
        trace = row[1 : len(x) + 1]
        yield name, trace


def _partial_scatter(x, y, name, **kwargs):
    return go.Scatter(x=x, y=y, name=name, showlegend=True, **kwargs)


def plot_stacked_area(x, model_output):
    return [
        _partial_scatter(x, y, name=name, mode="lines", stackgroup="one")
        for name, y in _prepare_rows(model_output, x)
        if "total" not in name.lower()
    ]


def plot_line(x, model_output):
    return [
        _partial_scatter(x, y, name, mode="lines+markers")
        for name, y in _prepare_rows(model_output, x)
        if "total" not in name.lower()
    ]


def plot_sankey(x, model_output):
    sources = []
    targets = []
    values = []
    for row in model_output[1::]:
        sources.append(row[0])
        targets.append(row[1])
        values.append(sum(row[2 : len(x) + 2]))

    nodes = list(set(sources + targets))
    sources = [nodes.index(source) for source in sources]
    targets = [nodes.index(target) for target in targets]

    return [
        go.Sankey(
            valueformat=".0f",
            valuesuffix="TWh",  # Get from Model2050Server.TABLE["Axis Unit"] ?
            node=dict(
                pad=15, thickness=15, line=dict(color="black", width=0.5), label=nodes,
            ),
            link=dict(source=sources, target=targets, value=values,),
        )
    ]


PLOTS_REGISTRY = {
    "stacked area with overlying line(s)": plot_stacked_area,
    "line": plot_line,
    "sankey/flow": plot_sankey,
}
