"""contains the Cog for Presence for the Bot"""
from discord.ext.commands import Bot, Cog
from discord import Activity
from contributor import AlbertUnruh


PRESENCE = Activity(type=2, name="dem Hackathon")


class PresenceCog(Cog, name="Presence"):
    """is a Cog for the Presence from the Bot"""

    contributor = [AlbertUnruh]

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def change_presence(self):
        """changes the presence to `PRESENCE`"""
        await self.bot.change_presence(activity=PRESENCE)
