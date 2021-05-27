"""
This is the main file from the Bot.

All contributors are listed in `contributor.py` with the URL to GitHub and
to the Discord Username and ID.
"""
from discord.ext.commands import Bot
from discord import Intents
from modules import register_commands
from CONFIGS import TOKEN, PREFIX
from contributor import print_contributor

from threading import Thread
from asyncio import run_coroutine_threadsafe, get_event_loop
from web_dashboard import run


intents = Intents.all()


bot = Bot(PREFIX, None, intents=intents, case_insensitive=True)
register_commands(bot)

run_coroutine_threadsafe(run(bot), get_event_loop())

print_contributor(bot)
bot.run(TOKEN)
