def test_model():
    from client_code.Model import language, levers, inputs, outputs, translate

    assert language == "en"
    assert levers[0] == "levers"
    assert inputs[0] == "inputs"
    assert outputs[0] == "outputs"
    assert translate("text") == ("translate", language, "text")
