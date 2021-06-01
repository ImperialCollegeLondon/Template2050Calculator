import json
from math import atan, pi, sin, sqrt
from pathlib import Path

import anvil.server
import i18n

from . import interface2050
from .model2050 import Model2050

model = Model2050(interface2050)

EARTH_RADIUS_KM = 6371


def arc_length_to_angle(length, radius):
    """Return the change in angle (in degrees) associated with a known arc length
    and radius.
    """
    return length / radius * (180 / pi)


def area_to_side_length(area, radius):
    """Return the side length for a square of known area on a spherical surface."""
    return 2 * radius * atan(sqrt(sin(area / (4 * radius ** 2))))


with open(Path(__file__).absolute().parent.parent / "web_outputs.json") as f:
    TABLE = json.load(f)


@anvil.server.callable
def lever_groups():
    return TABLE["output_lever_names_grouped"]


@anvil.server.callable
def calculate(inputs, start_year, end_year, expert_mode=False):
    solution = model.calculate(inputs, start_year, end_year)
    solution["output_emissions_sector"] = solution["output_emissions_sector"][-4::-1]
    solution["x"] = list(range(2015, 2105 if expert_mode else 2055, 5))
    return solution


i18n.set("filename_format", "{locale}.{format}")
i18n.set("enable_memoization", True)
i18n.load_path.append(Path(__file__).absolute().parent / "translations")


@anvil.server.callable
def translate(locale, text):
    i18n.set("locale", locale)
    return i18n.t(text)


@anvil.server.callable
def layout():
    return TABLE["weboutputs_summary_table"]


@anvil.server.callable
def map(data):
    import plotly.graph_objects as go

    fig = go.Figure()

    # the below will need to be configurable parameters
    start_draw_lat = 57.0
    start_draw_lon = -3.346
    padding = 0.20  # degrees
    map_center_lat = 55.3781
    map_center_lon = -3.436
    map_zoom = 4

    traces = []
    # draw areas starting with top-left corner at (start_draw_lat,start_draw_lon),
    # each subsequent box is placed to the south of the previous
    for name, area_km2 in data["area"]:
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
    for name, distance_km in data["distance"]:
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


@anvil.server.callable
def example_pathways():
    return TABLE["example_pathways"]


@anvil.server.callable
def default_inputs():
    return model.input_values_default()


@anvil.server.callable
def default_start_years():
    return model.start_values_default()


@anvil.server.callable
def default_end_years():
    return model.end_values_default()


@anvil.server.callable
def initial_values():
    return (
        lever_groups(),
        layout(),
        example_pathways(),
        default_inputs(),
        default_start_years(),
        default_end_years(),
    )
