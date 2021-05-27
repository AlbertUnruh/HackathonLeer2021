import CONFIGS
from os import environ

PASSWORD = environ.get("PASSWORD", None)
if PASSWORD is None:
    with open("PASSWORD") as pass:
        PASSWORD = pass.read()
