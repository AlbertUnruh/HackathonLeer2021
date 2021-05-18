from os import environ
from datetime import datetime


PREFIX = "h!"

# can be stored where ever you want :)
# at first the code checks if the is a environ variable,
# otherwise it read the token from a file
TOKEN = environ.get("DISCORD_BOT_TOKEN", None)
if TOKEN is None:
    with open("TOKEN") as f:
        TOKEN = f.read()


START_HACKATHON = datetime.fromisoformat("2021-05-18 15:20")
END_HACKATHON = datetime.fromisoformat("2021-05-18 15:30")
