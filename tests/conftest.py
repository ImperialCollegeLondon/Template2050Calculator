from unittest.mock import patch

from pytest import fixture


@fixture(autouse=True)
def patch_server_call():
    """This fixture simplifies testing by transparently removing the anvil
    server. Calling a callable from the front-end with this patch in place directly
    runs that function."""
    with patch("anvil.server.callable", lambda x: x):

        class ServerCallMock:
            def __call__(self, func_name, *args, **kwargs):
                from server_code import Model2050Server

                return getattr(Model2050Server, func_name)(*args, **kwargs)

        mocker = ServerCallMock()
        with patch("anvil.server.call", mocker):
            yield mocker
