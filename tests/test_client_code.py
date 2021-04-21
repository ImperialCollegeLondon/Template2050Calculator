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
    from client_code.Model import language, levers, inputs, outputs, translate

    assert language == "en"
    assert levers == ["Factor", "Offset"]
    assert np.all(inputs == [1, 1])
    assert outputs == ["a", "b", "lever_names"]

    assert translate("text") == "text"


def test_layout():
    from client_code.Model import layout
    from server_code.Model2050Server import GraphData

    overview = OrderedDict(
        (
            (
                "GHG Emissions / Primary Energy",
                OrderedDict(
                    (
                        (
                            "Top",
                            GraphData(
                                "Annual Greenhouse Gas Emissions",
                                "emissions_sector",
                            ),
                        ),
                        (
                            "Bottom",
                            GraphData(
                                "Primary Energy Consumption",
                                "primary_energy_consumption",
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
                            GraphData(
                                "Cumulative UK Greenhouse Gas Emissions",
                                "emissions_cumulative",
                            ),
                        ),
                        (
                            "Bottom",
                            GraphData(
                                "Final Energy Consumption",
                                "final_energy_consumption",
                            ),
                        ),
                    )
                ),
            ),
        )
    )

    assert overview == layout["Overview"]
