def test_model(patch_server_call):
    from client_code.Model import language, levers, inputs, outputs, translate

    assert language == "en"
    assert levers == "levers"
    assert inputs == "inputs"
    assert outputs == "outputs"

    assert translate("text") == ("translate", language, "text")
    patch_server_call.assert_called_with("translate", language, "text")
