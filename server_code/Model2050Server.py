import json
from math import atan, pi, sin, sqrt
from pathlib import Path

import anvil.server
import i18n
import yaml

from . import interface2050
from .model2050 import Model2050

EARTH_RADIUS_KM = 6371


def model():
    """The interface for running the model.

    Returns:
        Model2050: An initialised model.
    """
    return Model2050(interface2050)


def arc_length_to_angle(length, radius):
    """Return the change in angle (in degrees) associated with a known arc length
    and radius.
    """
    return length / radius * (180 / pi)


def area_to_side_length(area, radius):
    """Return the side length for a square of known area on a spherical surface."""
    return 2 * radius * atan(sqrt(sin(area / (4 * radius ** 2))))


BASE_DIR = Path(__file__).absolute().parent.parent
with open(BASE_DIR / "web_outputs.json") as f:
    TABLE = json.load(f)

with open(BASE_DIR / "app_config.yml") as f:
    CONFIG = yaml.safe_load(f)


@anvil.server.callable
def calculate(inputs, start_year, end_year, expert_mode=False):
    """Run the model in expert (2100) mode, or standard (2050) mode.

    Callable from the client side of the web app.

    Args:
        inputs (list): A list of all the ambition lever values.
        start_year (list): A list of the start year for each ambition lever.
        end_year (list): A list of the end year for each ambition lever.
        expert_mode (bool, optional): Flag to run in expert mode. Defaults to False.

    Returns:
        dict: A dictionary with lists for each output of the model and the years on the
            x axis (dictionary key is "x"). In 2050 mode the x axis will be from 2015 to
            2050 (inclusive) in steps of 5 years. 2100 mode will extend it to 2100.
    """
    solution = model().calculate(inputs, start_year, end_year)
    config = CONFIG["timeseries"]
    solution["x"] = list(
        range(config["start_year"], 2105 if expert_mode else 2055, config["step_size"])
    )
    return solution


i18n.set("filename_format", "{locale}.{format}")
i18n.set("enable_memoization", True)
i18n.load_path.append(Path(__file__).absolute().parent / "translations")


@anvil.server.callable
def translate(locale, text):
    """Stub for translating text to different languages. Requires a translation file.
    requires a dictionary/translation file to be added to the `server_code/translations`
    directory. The file will be named `<locale>.yml` and is a simple 1:1 translation.
    So every phrase to be translated must be included exactly as written, in full.

    Callable from the client side of the web app.

    Args:
        locale (str): The name of the language to translate to.
        text (str): The word/phrase to translate

    Returns:
        str: The translated text
    """
    i18n.set("locale", locale)
    return i18n.t(text)


@anvil.server.callable
def map(data):
    """Generate the figure for the map plot. Currently centred over the UK.

    Callable from the client side of the web app.

    Args:
        data (dict): Contains the filled areas and distances to plot on the map.

    Returns:
        go.Figure: The plotly figure with the map and the filled areas.
    """
    import plotly.graph_objects as go

    fig = go.Figure()

    map_config = CONFIG["maps"]
    start_draw_lat = map_config["start_draw_lat"]
    start_draw_lon = map_config["start_draw_lon"]
    padding = map_config["padding"]  # degrees
    map_center_lat = map_config["map_center_lat"]
    map_center_lon = map_config["map_center_lon"]
    map_zoom = map_config["map_zoom"]

    traces = []
    # draw areas starting with top-left corner at (start_draw_lat,start_draw_lon),
    # each subsequent box is placed to the south of the previous
    areas = data.get("area", [])
    for name, area_km2 in areas:
        length_km = area_to_side_length(area_km2, EARTH_RADIUS_KM)
        d_theta_deg = arc_length_to_angle(length_km, EARTH_RADIUS_KM)

        # box coordinates below are clockwise from top-left
        lats = [
            start_draw_lat,
            start_draw_lat,
            start_draw_lat - d_theta_deg,
            start_draw_lat - d_theta_deg,
        ]
        lons = [
            start_draw_lon,
            start_draw_lon + d_theta_deg,
            start_draw_lon + d_theta_deg,
            start_draw_lon,
        ]
        traces.append(
            go.Scattermapbox(fill="toself", lon=lons, lat=lats, name=name, mode="lines")
        )
        if area_km2:
            start_draw_lat -= d_theta_deg + padding

    # now draw lines for distance quantities in a similar fashion
    distances = data.get("distances", [])
    for name, distance_km in distances:
        d_theta_deg = arc_length_to_angle(distance_km, EARTH_RADIUS_KM)
        lats = [start_draw_lat, start_draw_lat]
        lons = [start_draw_lon, start_draw_lon + d_theta_deg]
        traces.append(
            go.Scattermapbox(lon=lons, lat=lats, name=name, mode="lines+markers")
        )
        if distance_km:
            start_draw_lat -= padding

    fig = go.Figure(
        traces,
        layout=dict(
            mapbox={
                "style": "stamen-terrain",
                "center": {"lat": map_center_lat, "lon": map_center_lon},
                "zoom": map_zoom,
            },
        ),
    )
    return fig


def lever_groups():
    """Return the groups names and tooltips of the ambition levers."""
    return TABLE["output_lever_names_grouped"]


def layout():
    """Return the details of the layout - ie the Web Outputs Summary Table."""
    return TABLE["weboutputs_summary_table"]


def example_pathways():
    """Return the lever values for the example pathways in the model."""
    return TABLE["example_pathways"]


def default_inputs():
    """Return the default lever values of the model."""
    return model().input_values_default()


def default_start_years():
    """Return the default start year values of the model."""
    start_years = model().start_values_default()
    if any(year < CONFIG["2100_mode"]["min_year"] for year in start_years):
        raise ValueError("Invalid default start year value")
    return start_years


def default_end_years():
    """Return the default end year values of the model."""
    end_years = model().end_values_default()
    if any(year > CONFIG["2100_mode"]["max_year"] for year in end_years):
        raise ValueError("Invalid default end year value")
    return end_years


@anvil.server.callable
def initial_values():
    """Return the initial values for when loading the web app.

    Callable from the client side of the web app.
    """
    return dict(
        lever_groups=lever_groups(),
        layout=layout(),
        example_pathways=example_pathways(),
        default_inputs=default_inputs(),
        default_start_years=default_start_years(),
        default_end_years=default_end_years(),
        expert_mode_range=CONFIG["2100_mode"],
        expert_mode=CONFIG["2100_mode"],
        maps_data_year=CONFIG["maps"]["data_year"],
        sankey_data_year=CONFIG["sankey"]["data_year"],
    )
