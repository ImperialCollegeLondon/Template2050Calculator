from pytest import fixture
from unittest.mock import patch


@fixture(autouse=True)
def patch_server_call():
    with patch("anvil.server.call", lambda *x: x):
        yield
