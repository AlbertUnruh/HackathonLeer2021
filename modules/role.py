"""contains cog for role functions"""
from discord.ext.commands import Bot, Cog, Context, command
from discord import Role, CategoryChannel, PermissionOverwrite, Embed
from discord.utils import get
from typing import Optional
from contributor import MikeCodes2586
from CONFIGS import PREFIX
from database import User

class RoleCog(Cog, name="RoleManager"):
    """is a cog with funtions for creating, deleting and destributing roles"""

    contributor = [MikeCodes2586]

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="make_team")
    async def create_team(self, ctx: Context, *name: str):
        """creates a role, category, a text and a voice channel for a team and gives the author the role"""

        team_name = " ".join(name)
        user = User.get_users(id=ctx.author.id)[0]
        if user[6] != team_name:
            embed: Embed = Embed(color=0x5865F2, title="Fehler")
            embed.add_field(name= "Nicht in Team", value= f"Melde dich in einem DM-Channel mit `{self.bot.user}` mit `{PREFIX}anmelden` an")
            await ctx.channel.send(embed=embed)
            return

        team_role: Role = await self.bot.guilds[0].create_role(name=team_name)

        await self.bot.guilds[0].get_member(ctx.author.id).add_roles(team_role)

        t_cat_overwrites = {
            self.bot.guilds[0].default_role: PermissionOverwrite(**{
                "view_channel": False
            }),
            team_role: PermissionOverwrite(**{
                "view_channel": True
            })
        }
        team_category: CategoryChannel = await self.bot.guilds[0].create_category(
            name=team_name, overwrites=t_cat_overwrites)

        t_cha_overwrites = {
            self.bot.guilds[0].default_role: PermissionOverwrite(**{
                "view_channel": False
            }),
            team_role: PermissionOverwrite(**{
                "view_channel": True
            })
        }
        await self.bot.guilds[0].create_text_channel(name="Text Channel",
                                                     overwrites=t_cha_overwrites,
                                                     category=team_category)

        await self.bot.guilds[0].create_voice_channel(name="Voice Channel",
                                                      overwrites=t_cha_overwrites,
                                                      category=team_category)

    @command(name="remove_team")
    async def remove_team(self, ctx: Context,
                          category: Optional[CategoryChannel] = None):
        """deletes a category with the channels inside"""
        if category is None:
            await ctx.channel.send(f"Bitte gebe einen richtigen Teamnamen an! \nAchte auf Großschreibung \nNutzung: `{PREFIX}remove_team [dein team name]` (in \" \" wenn er Leerzeichen hat)")
            return

        user = User.get_users(id=ctx.author.id)[0]
        if user[6] != category.name:
            embed: Embed = Embed(color=0x5865F2, title="Fehler")
            embed.add_field(name= "Nicht in Team", value= f"Melde dich in einem DM-Channel mit `{self.bot.user}` mit `{PREFIX}anmelden` an")
            await ctx.channel.send(embed=embed)
            return

        if not ctx.author.guild_permissions.manage_roles:
            await ctx.channel.send("Du hast nicht genug perms!")
            return

        await (get(self.bot.guilds[0].roles, name=category.name)).delete()

        for channel in category.channels:
            await channel.delete()
        await category.delete()

    @command(name="join_team")
    async def give_author_role(self, ctx: Context, role: Optional[Role] = None):
        """gives the author the selected role"""

        user = User.get_users(id=ctx.author.id)[0]
        if user[6] != role.name:
            embed: Embed = Embed(color=0x5865F2, title="Fehler")
            embed.add_field(name= "Nicht in Team", value= f"Melde dich in einem DM-Channel mit `{self.bot.user}` mit `{PREFIX}anmelden` an")
            await ctx.channel.send(embed=embed)
            return

        await self.bot.guilds[0].get_member(ctx.author.id).add_roles(role)

        if role in ctx.author.roles:
            await ctx.channel.send("Es hat funtioniert!")
        elif role not in ctx.author.roles:
            await ctx.channel.send("Etwas ist falsch gelaufen und du hast die Rolle nicht bekommen. \nVersuchs nochmal!")
        else:
            await ctx.channel.send("Irgendwas ist seehr falsch gelaufen. Bitte kontaktiere einen Dev.")

    @command(name="exit_team")
    async def remove_author_role(self, ctx: Context,
                              role: Optional[Role] = None):
        """gives the author the selected role"""

        await self.bot.guilds[0].get_member(ctx.author.id).remove_roles(role)

        if role not in ctx.author.roles:
            await ctx.channel.send("Es hat funtioniert!")
        elif role in ctx.author.roles:
            await ctx.channel.send("Etwas ist falsch gelaufen und du hast die Rolle immer noch. \nVersuchs nochmal!")
        else:
            await ctx.channel.send("Irgendwas ist seehr falsch gelaufen. Bitte kontaktiere einen Dev.")

    @command(name="check_team")
    async def check_for_team_in_DB(self, ctx: Context,
                                  *name: str):
        """checks if the given team is in the database"""

        team_name = " ".join(name)
        team = User.get_users(team=team_name)

        if not team:
            await ctx.channel.send(f"Das Team gibt es nicht (achte auf Großschreibung). \nDu kannst ein Team mit `{PREFIX}make_team mein teamname`(Leerzeichen möglich) erstellen wenn du die `manage_roles` permission hast.")
            return
        await ctx.channel.send(f"Das Team existiert und hat {len(team)} Mitglieder")

