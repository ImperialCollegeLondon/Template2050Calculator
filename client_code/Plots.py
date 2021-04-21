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
    ]


def plot_line(x, model_output):
    return [
        _partial_scatter(x, y, name, mode="lines+markers")
        for name, y in _prepare_rows(model_output, x)
    ]


PLOTS_REGISTRY = {
    "stacked area with overlying line(s)": plot_stacked_area,
    "line": plot_line,
}
