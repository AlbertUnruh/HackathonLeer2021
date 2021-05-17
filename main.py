from discord.ext.commands import Bot
from discord import Intents
from modules import register_commands
from CONFIGS import *


intents = Intents.all()


bot = Bot(PREFIX, None, None, intents=intents, case_insensitive=False)
register_commands(bot)

bot.run(TOKEN)
