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
        embed.add_field(name= "Suche", value= "Du brauchst Hilfe? Dann wähle eine Suchmaschine aus: \n> -ddg | duckduckgo | browse | search | s \n> -gh | github \n> -g | google \n> -sof | stackoverflow \n> -ecosia \n> -bing", inline=True)
        embed.add_field(name= "Teams", value= "So erstellst du ein neues Team: \n> make_team Teamname \n> (Der Teamname darf auch Leerzeichen enthalten) \n \n So löscht du ein Team: \n> remove_team Teamname \n \n Wenn es dein Team schon gibt kannst du so joinen: \n> join_team Teamname \n \n Du willst lieber in ein anderes Team? Dann verlasse dein Team einfach: \n> exit_team Teamname", inline=True)
        embed.add_field(name= "Anmelden", value= 'Um dich anzumelden schreibe dem Bot im Privatchat: \n> anmelden "E-Mail" "Name" "Schule" "Klasse" "Teamname"', inline=False)



        await ctx.channel.send(embed=embed)