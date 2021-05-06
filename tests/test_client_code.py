import json
import sys
from collections import OrderedDict
from pathlib import Path
from unittest.mock import patch

import numpy as np

sys.path.append(str(Path(__file__).absolute().parent / "test_model"))

import interface2050  # noqa: E402

with open(Path(__file__).absolute().parent / "test_model" / "web_outputs.json") as f:
    TABLE = json.load(f)

INTERFACE_PATCHER = patch("server_code.interface2050", interface2050, create=True)
TABLE_PATCHER = patch("server_code.Model2050Server.TABLE", TABLE)


def setup_module():
    INTERFACE_PATCHER.start()
    TABLE_PATCHER.start()


def teardown_module():
    INTERFACE_PATCHER.stop()
    TABLE_PATCHER.stop()


def test_model(patch_server_call):
    from client_code.Model import inputs, language, lever_groups, outputs, translate

    assert language == "en"
    assert np.all(inputs == [1, 1])
    assert outputs == ["a", "b", "lever_names"]

    assert translate("text") == "text"

    assert lever_groups["group1"] == {
        "names": ["name1", "name2"],
        "tooltips": [
            ["label_tip", "button_tip1", "button_tip2", "button_tip4", "button_tip4"],
            ["label_tip", "button_tip1", "button_tip2", "button_tip4", "button_tip4"],
        ],
    }


def test_layout():
    from client_code.Model import GraphInfo, layout

    overview = OrderedDict(
        (
            (
                "GHG Emissions / Primary Energy",
                OrderedDict(
                    (
                        (
                            "Top",
                            GraphInfo(
                                "Annual Greenhouse Gas Emissions",
                                "emissions_sector",
                                "Stacked Area with overlying Line(s)",
                            ),
                        ),
                        (
                            "Bottom",
                            GraphInfo(
                                "Primary Energy Consumption",
                                "primary_energy_consumption",
                                "Stacked Area with overlying Line(s)",
                            ),
                        ),
                    )
                ),
            ),
            (
                "GHG Cumulative / Final Energy",
                OrderedDict(
                    (
                        (
                            "Top",
                            GraphInfo(
                                "Cumulative UK Greenhouse Gas Emissions",
                                "emissions_cumulative",
                                "Line",
                            ),
                        ),
                        (
                            "Bottom",
                            GraphInfo(
                                "Final Energy Consumption",
                                "final_energy_consumption",
                                "Stacked Area with overlying Line(s)",
                            ),
                        ),
                    )
                ),
            ),
        )
    )

    assert overview == layout["Overview"]
