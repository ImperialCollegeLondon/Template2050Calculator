# Template2050Calculator

For this web app to work, the compiled python interface of a 2050 Calculator model needs to be included. This is done by running the [Mackay Python Interface](https://github.com/ImperialCollegeLondon/mackay_python_interface) and adding the two files `interface.py` and `_interface2050.*.so` into the `server_code` directory.

It can be run locally in a Python virtual environment. Install the `requirements.txt` and run `anvil-app-server --app Template2050Calculator` from the _parent directory_ of this repo. Additionally, Java is required to run the anvil app server.

The app can be run from within a docker container by running `docker-compose up`.
