"""this is the Cog to display the contributors from the Cogs on Discord"""
from discord.ext.commands import Bot, Cog, Context, command
from discord import Embed
from contributor import AlbertUnruh, sorted_contributors


class ContributorCog(Cog, name="Contributor"):
    """is a Cog for the Ping from the Bot"""

    contributor = [AlbertUnruh]

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="contributor", aliases=["mitwirkende"])
    async def contributor(self, ctx: Context):
        """displays the contributor"""
        embed: Embed = Embed(title="Unsere Mitwirkenden",
                             description="Hier sind alle, die am Bot gearbeitet haben aufgelistet")

        for contributor in sorted_contributors(self.bot):
            embed.add_field(name=f"__{contributor.name}__",
                            value=f"> <@{contributor.id}>\n"
                                  f"> [GitHub]({contributor.github} \"Hier geht es zu GitHub\")")

        await ctx.send(embed=embed)
