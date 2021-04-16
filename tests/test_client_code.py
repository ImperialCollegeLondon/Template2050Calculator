import sys
from pathlib import Path
from unittest.mock import patch

import numpy as np

sys.path.append(str(Path(__file__).absolute().parent / "test_model"))

import interface2050  # noqa: E402

PATCHER = patch("server_code.interface2050", interface2050, create=True)


def setup_module():
    PATCHER.start()


def teardown_module():
    PATCHER.stop()


def test_model(patch_server_call):
    from client_code.Model import language, levers, inputs, outputs, translate

    assert language == "en"
    assert levers == ["Factor", "Offset"]
    assert np.all(inputs == [1, 1])
    assert outputs == ["a", "b", "lever_names"]

    assert translate("text") == "text"


def test_layout():
    from client_code.Model import layout

    assert layout["Overview"] == [
        "GHG Emissions / Primary Energy",
        "GHG Cumulative / Final Energy",
    ]
    assert layout["Imports, Map & Flows"] == ["Imports", "Map", "Flows"]
