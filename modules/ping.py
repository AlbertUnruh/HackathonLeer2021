"""contains the Cog for the Bot-Ping and latency"""
from discord.ext.commands import Bot, Cog, Context, command
from discord import Embed
from datetime import datetime
from contributor import AlbertUnruh


PATTERN = "> {} Sekunden"


class PingCog(Cog, name="Ping"):
    """is a Cog for the Ping from the Bot"""

    contributor = [AlbertUnruh]

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="ping", aliases=["pong", "latency", ":ping_pong:", "🏓"])
    async def ping(self, ctx: Context):
        """checks the ping"""
        embed: Embed = Embed(title=f"🏓 {'Ping' if ctx.invoked_with.lower() == 'pong' else 'Pong'}",
                             description="Hier sind die Latenzen aufgelistet:",
                             timestamp=datetime.utcnow())

        embed.add_field(name="API", value=self.api())
        embed.add_field(name="Nachricht", value=self.time(ctx.message.created_at))

        embed.set_footer(text="Die Latenz von `Nachricht` kann negativ sein, wenn die Systemuhr nicht mit der Zeit von Discord übereinstimmt.")

        await ctx.send(embed=embed)

    def api(self) -> str:
        """the ping from the API"""
        return PATTERN.format(round(self.bot.latency, 2))

    @staticmethod
    def time(time: datetime) -> str:
        """the difference from `time` to now"""
        return PATTERN.format(round((datetime.utcnow() - time).total_seconds(), 2))
