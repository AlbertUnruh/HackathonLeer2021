"""
This is the main file from the Bot.

All contributors are listed in `contributor.py` with the URL to GitHub and
to the Discord Username and ID.
"""
from discord.ext.commands import Bot
from discord import Intents
from modules import register_commands
from CONFIGS import *
from contributor import print_contributor


intents = Intents.all()


bot = Bot(PREFIX, None, intents=intents, case_insensitive=False)
register_commands(bot)

print_contributor(bot)
bot.run(TOKEN)
