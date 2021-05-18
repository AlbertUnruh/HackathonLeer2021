from discord.ext.commands import Bot, Cog, command, Context
from urllib.parse import quote


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


class BrowserCog(Cog, name="Browser"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="ddg", aliases=["duckduckgo", "browse", "search", "s"])
    async def ddg(self, ctx: Context, *query: str):
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_DDG.format(query=query)))

    @command(name="gh", aliases=["github"])
    async def gh(self, ctx: Context, *query: str):
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_G.format(query=query)))

    @command(name="sof", aliases=["stackoverflow"])
    async def sof(self, ctx: Context, *query: str):
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_G.format(query=query)))

    @command(name="g", aliases=["google"])
    async def g(self, ctx: Context, *query: str):
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_G.format(query=query)))

    @command(name="ecosia", aliases=[])
    async def ecosia(self, ctx: Context, *query: str):
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_ECOSIA.format(query=query)))

    @command(name="bing", aliases=[])
    async def bing(self, ctx: Context, *query: str):
        query = quote(" ".join(query)) or DEFAULT_SEARCH
        await ctx.send(MSG.format(url=URL_BING.format(query=query)))