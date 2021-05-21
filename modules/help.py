from discord.ext.commands import Bot, Cog, command, Context
from contributor import Nxnx0502
from discord import Embed

class HelpCog(Cog, name="Help"):
    contributor=[Nxnx0502]

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="help", aliases=["Help"])
    async def helpcommand(self, ctx: Context):
        embed: Embed = Embed(color=0x5865F2, title="Hilfe")
        embed.add_field(name= "Suche", value= "Commands: \n> s \n> ddg", inline= True)
        embed.add_field(name= "Teams", value= "Commands: \n> make_team Beispiel-name(Leerzeichen möglich)", inline= True)

        await ctx.channel.send(embed=embed)