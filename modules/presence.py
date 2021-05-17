from discord.ext.commands import Bot, command, Cog
from discord import Status, Activity


PRESENCE = "to the winners :)"


class PresenceCog(Cog, name="Presence"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def change_presence(self):
        await self.bot.change_presence(activity=Activity(name=PRESENCE, type=2))
