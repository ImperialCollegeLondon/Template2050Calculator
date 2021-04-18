import anvil.server

# This is a module.
# You can define variables and functions here, and use them from any form.

levers = anvil.server.call("levers")
inputs = anvil.server.call("inputs")
outputs = anvil.server.call("outputs")
layout = anvil.server.call("layout")
lever_descriptions = anvil.server.call("lever_descriptions")

language = "en"


# Use this to translate - later add a registration so all text can be translated at once
def translate(text):
    return anvil.server.call("translate", language, text)
