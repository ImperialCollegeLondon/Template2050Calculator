from pytest import mark

# Skip this test module when the interface2050 module is unavailable (currently in ci)
# In future, should be able to pull in the interface from a docker image
try:
    import server_code.interface2050  # noqa: F401
except ImportError:
    pytestmark = mark.skipif(True, reason="No interface module available.")


def test_inputs():
    import numpy as np
    from server_code.Model2050Server import inputs

    assert isinstance(inputs(), np.ndarray)
