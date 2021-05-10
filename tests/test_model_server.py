import sys
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).absolute().parent / "test_model"))

import interface2050  # noqa: E402

PATCHER = patch("server_code.interface2050", interface2050, create=True)


def setup_module():
    PATCHER.start()


def teardown_module():
    PATCHER.stop()
