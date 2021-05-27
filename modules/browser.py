"""contains the Cog for internet research"""
from discord.ext.commands import Bot, Cog, command, Context
from urllib.parse import quote
from contributor import AlbertUnruh


MSG = """\
Hier ist eine Suche für deine Frage:
{url}
"""
DEFAULT_SEARCH = "Covid19"

URL_DDG:    str = "https://duckduckgo.com/?q={query}"  # is the default
URL_GH:     str = "https://github.com/search?q={query}"
URL_SOF:    str = "https://stackoverflow.com/search?q={query}"
URL_G:      str = "https://www.google.com/search?q={query}"
URL_ECOSIA: str = "https://www.ecosia.org/search?q={query}"
URL_BING:   str = "https://www.bing.com/search?q={query}"
URL_LIVE_Y: str = "https://www.youtube.com/channel/UCkeTyOUOKObW1pNlfptzC2A"
URL_LIVE_T: str = "https://www.twitch.tv/hackathonleer"


class BrowserCog(Cog, name="Browser"):
    """is a Cog for the Browser function from the Bot"""

    contributor = [AlbertUnruh]

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="ddg", aliases=["duckduckgo", "browse", "search", "s"])
    async def ddg(self, ctx: Context, *query: str):
        """is the DuckDuckGo/default search"""
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_DDG.format(query=query)))

    @command(name="gh", aliases=["github"])
    async def gh(self, ctx: Context, *query: str):
        """is the GitHub search"""
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_G.format(query=query)))

    @command(name="sof", aliases=["stackoverflow"])
    async def sof(self, ctx: Context, *query: str):
        """is the StackOverFlow search"""
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_G.format(query=query)))

    @command(name="g", aliases=["google"])
    async def g(self, ctx: Context, *query: str):
        """is the Google search"""
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_G.format(query=query)))

    @command(name="ecosia", aliases=[])
    async def ecosia(self, ctx: Context, *query: str):
        """is the Ecosia search"""
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_ECOSIA.format(query=query)))

    @command(name="bing", aliases=[])
    async def bing(self, ctx: Context, *query: str):
        """is the Bing search"""
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_BING.format(query=query)))

    @command(name="live", aliases=[])
    async def live(self, ctx: Context):
        """displays the live-streaming-channels"""
        await ctx.send(f"Hier ist der Link zu "
                       f"[YouTube]({URL_LIVE_Y} {URL_LIVE_Y}) "
                       f"und zu "
                       f"[Twitch]({URL_LIVE_T} {URL_LIVE_T}),\n"
                       f"viel spaß beim Zuschauen!")
