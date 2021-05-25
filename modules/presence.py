"""contains the Cog for Presence for the Bot"""
from discord.ext.commands import Bot, Cog
from discord import Activity, Member
from contributor import AlbertUnruh
from colorama import Fore as Fg, Style
from CONFIGS import PREFIX


PRESENCE = Activity(type=2, name="dem Hackathon")
LOGGED_IN = Fg.GREEN + "We are logged in as " + Fg.YELLOW + "%s" \
            + Fg.GREEN + "!" + Style.RESET_ALL
PATTERN_PREFIX = "[{0}]"
PATTERN_NAME = "{1.display_name}"
PATTERN = " ".join([PATTERN_PREFIX, PATTERN_NAME])


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

    @Cog.listener("on_ready")
    async def nick(self):
        """updates the nickname from the Bot"""
        me: Member = self.bot.guilds[0].me
        if not me.display_name.startswith(PATTERN_PREFIX.format(PREFIX)):
            await me.edit(nick=PATTERN.format(PREFIX, me))
