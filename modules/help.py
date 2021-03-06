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
                             description=f"Mein Präfix ist `{CONFIGS.PREFIX}`\n"
                                         f"_Notiz: die Befehle beinhalten __keinen__ Zeilenumbruch_")

        embed.add_field(name="Suche", value="""\
Du brauchst Hilfe? Dann wähle eine Suchmaschine aus:
> `browse`, `search`, `s`, `duckduckgo`, `ddg`, `github`, `gh`, `google`, `g`, `stackoverflow`, `sof`, `ecosia`, `bing`""")

        embed.add_field(name="Anmelden", value="""\
Du willst beim Hackathon teilnehmen oder? Dann schreibe dem Bot im Privatchat:
> `anmelden "E-Mail" "Name" "Schule" "Klasse" "Teamname"`""")

        embed.add_field(name="Mitwirkende", value="""\
Du willst wissen wer bei diesem Bot Mist gebaut hat? So kriegst du die Namen für die Beschwerde raus:
> `contributors`""")

        if self.bot.guilds[0].get_member(ctx.author.id).guild_permissions.manage_roles:
            embed.add_field(name="Team checken", value="""\
Wenn du dir nicht sicher bist, ob dein Team schon existiert, guck einfach nach:
> `check_team TEAMNAME`""")

        embed.add_field(name="Abmelden", value="""\
Du hast es dir doch anders überlegt? So kannst du dich wieder vom Hackathon abmelden:
> `abmelden`""")

        if self.bot.guilds[0].get_member(ctx.author.id).guild_permissions.manage_roles:
            embed.add_field(name="Team löschen", value="""\
So löscht du ein Team:
> `remove_team TEAMNAME`""")

        embed.add_field(name="Livestream", value="""\
Du hast kein Bock den Livestream rauszusuchen? Lass den Bot das für dich tun:
> `live`""")

        embed.add_field(name="Latenz", value="""\
Hier sind die Latenzen zusehen:
> `ping`, `pong`""")

        await ctx.channel.send(embed=embed)
