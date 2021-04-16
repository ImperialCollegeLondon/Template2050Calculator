from pytest import fixture
from unittest.mock import MagicMock, patch


@fixture(autouse=True)
def patch_server_call():
    def side_effect(*args):
        if len(args) == 0:
            return None
        if len(args) == 1:
            return args[0]
        return args

    mocker = MagicMock(side_effect=side_effect)
    with patch("anvil.server.call", mocker):
        yield mocker
