"""contains the Cog for Presence for the Bot"""
from discord.ext.commands import Bot, Cog
from discord import Activity
from contributor import AlbertUnruh
from colorama import Fore as Fg, Style


PRESENCE = Activity(type=2, name="dem Hackathon")
LOGGED_IN = Fg.GREEN + "We are logged in as " + Fg.YELLOW + "%s" \
            + Fg.GREEN + "!" + Style.RESET_ALL


class PresenceCog(Cog, name="Presence"):
    """is a Cog for the Presence from the Bot"""

    contributor = [AlbertUnruh]

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def change_presence(self):
        """changes the presence to `PRESENCE`"""
        await self.bot.change_presence(activity=PRESENCE)

    @Cog.listener("on_ready")
    async def logged_in(self):
        """prints out the user at which the Bot is logged in"""
        print(LOGGED_IN % self.bot.user)
