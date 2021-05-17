from discord.ext.commands import Bot
from discord import Intents
from CONFIGS import *


intents = Intents.all()


bot = Bot(PREFIX, help_command=None, description=None, intents=intents)
