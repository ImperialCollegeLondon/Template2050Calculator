import json
import sys
from collections import OrderedDict
from pathlib import Path
from unittest.mock import patch

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
    from client_code.Model import init_vals, language, translate

    assert language == "en"
    assert translate("text") == "text"

    assert init_vals["lever_groups"]["group1"] == {
        "names": ["name1", "name2"],
        "tooltips": [
            ["label_tip", "button_tip1", "button_tip2", "button_tip4", "button_tip4"],
            ["label_tip", "button_tip1", "button_tip2", "button_tip4", "button_tip4"],
        ],
    }


def test_layout():
    from client_code.Model import GraphInfo, init_vals

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
                                "output_emissions_sector",
                                "Stacked Area with overlying Line(s)",
                                "MtCO2e/yr",
                            ),
                        ),
                        (
                            "Bottom",
                            GraphInfo(
                                "Primary Energy Consumption",
                                "output_primary_energy_consumption",
                                "Stacked Area with overlying Line(s)",
                                "TWh/yr",
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
                                "output_emissions_cumulative",
                                "Line",
                                "MtCO2e",
                            ),
                        ),
                        (
                            "Bottom",
                            GraphInfo(
                                "Final Energy Consumption",
                                "output_final_energy_consumption",
                                "Stacked Area with overlying Line(s)",
                                "TWh/yr",
                            ),
                        ),
                    )
                ),
            ),
        )
    )

    assert overview == init_vals["layout"]["Overview"]
