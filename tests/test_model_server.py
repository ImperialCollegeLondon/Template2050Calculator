def test_inputs():
    import numpy as np
    from server_code.Model2050Server import inputs

    assert isinstance(inputs(), np.ndarray)
