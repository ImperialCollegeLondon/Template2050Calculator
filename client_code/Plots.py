import plotly.graph_objects as go

PLOTS_REGISTRY = {}
"""Registry of known plots"""


def _register_plot(func=None, plot_type=None):
    """Register a plot."""
    if func is None:
        return lambda f: _register_plot(f, plot_type=plot_type)

    plot_type = plot_type if plot_type else func.__name__
    PLOTS_REGISTRY[plot_type] = func

    return func


def _prepare_rows(data, x):
    for row in data[::-1]:
        name = row[0]
        trace = row[1 : len(x) + 1]
        yield name, trace


def _partial_scatter(x, y, plot_type):
    return lambda **kwargs: go.Scatter(
        x=x, y=y, plot_type=plot_type, showlegend=True, **kwargs
    )


@_register_plot(plot_type="stacked area with overlying line(s)")
def plot_stacked_area(x, model_output):
    return [
        _partial_scatter(x, y, plot_type)(mode="lines", stackgroup="one")
        for plot_type, y in _prepare_rows(model_output, x)
    ]


@_register_plot(plot_type="line")
def plot_line(x, model_output):
    return [
        _partial_scatter(x, y, plot_type)(mode="lines+markers")
        for plot_type, y in _prepare_rows(model_output, x)
    ]
