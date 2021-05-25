"""contains the Cog for the Help cmd"""
from discord.ext.commands import Bot, Cog, command, Context
from contributor import Nxnx0502
from discord import Embed
import CONFIGS


class HelpCog(Cog, name="Help"):
    """is the COg for the Help"""
    contributor = [Nxnx0502]

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="help", aliases=["h"])
    async def helpcommand(self, ctx: Context):
        """displays the help"""
        embed: Embed = Embed(color=0x5865F2, title="Hilfe",
                             description=f"Mein Präfix ist `{CONFIGS.PREFIX}`")

        embed.add_field(name="Suche", value="""\
Du brauchst Hilfe? Dann wähle eine Suchmaschine aus:
> -ddg | duckduckgo | browse | search | s
> -gh | github
> -g | google
> -sof | stackoverflow
> -ecosia
> -bing""")

        embed.add_field(name="Teams", value="""\
So erstellst du ein neues Team:
> make_team Teamname
> (Der Teamname darf auch Leerzeichen enthalten)

So löscht du ein Team:
> remove_team Teamname

Wenn es dein Team schon gibt kannst du so joinen:
> join_team Teamname

Dein Team nervt? Dann verlasse dein Team einfach:
> exit_team Teamname""")

        embed.add_field(name="Anmelden", value="""\
Um dich anzumelden schreibe dem Bot im Privatchat:
> anmelden "E-Mail" "Name" "Schule" "Klasse" "Teamname" """)

        embed.add_field(name="Latenz", value="""\
Hier sind die Latenzen zusehen:
> :ping_pong:""")

        embed.add_field(name="Mitwirkende", value="""\
Du willst wissen wer bei diesem Bot Mist gebaut hat? So kriegst du die Namen für die Beschwerde raus:
> contributer""")

        await ctx.channel.send(embed=embed)
