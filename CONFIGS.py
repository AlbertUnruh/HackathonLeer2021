"""here are all the configurations stored for the code"""
from os import environ


# is the prefix for the Bot-Commands
PREFIX = "h!"


# here are all Roles listed, which are ignored by the Bot
# and if some tries to use them, `BLACKLISTED_MSG` 'll be displayed
# ..note::
#     Categories from the Server should also be listed here!
BLACKLISTED_ROLES = (
    "Admin",                    # Admin Role
    "everyone",                 # Discord Role
    "here",                     # Discord Role
    "Textkanäle",               # Discord Category
    "Allgemeine Sprachkanäle",  # Discord Category
    "Das war: 2020",            # Discord Category
    "Das war: 2021",            # Discord Category
)

# `role` should be a instance of :class:`str`
BLACKLISTED_MSG = "Hey, ich denke mein Name ist Hase und ich kenne die Rolle `{role}` nicht..."


# can be stored where ever you want :)
# at first the code checks if the is a environ variable,
# otherwise it read the token from a file
TOKEN = environ.get("DISCORD_BOT_TOKEN", None)
if TOKEN is None:
    with open("TOKEN") as f:
        TOKEN = f.read()
