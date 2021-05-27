import CONFIGS
from os import environ

SECRET_KEY = environ.get("SECRET_KEY", None)
if SECRET_KEY is None:
    with open("SECRET_KEY") as f:
        SECRET_KEY = f.read()

DISCORD_CLIENT_SECRET = environ.get("DISCORD_CLIENT_SECRET", None)
if DISCORD_CLIENT_SECRET is None:
    with open("DISCORD_CLIENT_SECRET") as f:
        DISCORD_CLIENT_SECRET = f.read()

DISCORD_REDIRECT_URI = environ.get("DISCORD_REDIRECT_URI", None)
if DISCORD_REDIRECT_URI is None:
    with open("DISCORD_REDIRECT_URI") as f:
        DISCORD_REDIRECT_URI = f.read()

DISCORD_CLIENT_ID = 843893717907406898

DISCORD_BOT_TOKEN = CONFIGS.TOKEN
