from discord.ext.commands import Bot, Cog
from discord import Activity


PRESENCE = Activity(type=2, name="den Hackathon")


class PresenceCog(Cog, name="Presence"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def change_presence(self):
        await self.bot.change_presence(activity=PRESENCE)
