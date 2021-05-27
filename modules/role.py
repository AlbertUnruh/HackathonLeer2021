"""contains cog for role functions"""
from discord.ext.commands import Bot, Cog, Context, command
from discord import Role, CategoryChannel, PermissionOverwrite, Member
from discord.utils import get
from typing import Optional
from contributor import MikeCodes2586, AlbertUnruh
from CONFIGS import PREFIX
from database import DbUser
from re import compile
from random import randint
from typing import Callable


__all__ = (
    "RoleCog",
    "Ext",
    "get_color",
)


VALID_CHARS = compile(r"[a-zA-Z0-9_.+\- äöü]")
get_color: Callable[[], int] = lambda: randint(0x000000, 0xFFFFFF)


class Ext:
    """is a extension from the RoleCog"""

    contributor = [AlbertUnruh]

    @staticmethod
    async def create_team(bot: Bot, team: str, author: Member) -> Role:
        """creates a new team"""
        team_role: Optional[Role] = get(bot.guilds[0].roles, name=team)
        if team_role is not None:
            return team_role

        team_role: Role = await bot.guilds[0].create_role(name=team,
                                                          color=get_color())

        await bot.guilds[0].get_member(author.id).add_roles(team_role)

        t_cat_overwrites = {
            bot.guilds[0].default_role: PermissionOverwrite(**{
                "view_channel": False
            }),
            team_role: PermissionOverwrite(**{
                "view_channel": True
            })
        }
        team_category: CategoryChannel = await bot.guilds[
            0].create_category(
            name=team, overwrites=t_cat_overwrites)

        t_cha_overwrites = {
            bot.guilds[0].default_role: PermissionOverwrite(**{
                "view_channel": False
            }),
            team_role: PermissionOverwrite(**{
                "view_channel": True
            })
        }
        await bot.guilds[0].create_text_channel(name="Team Chat",
                                                overwrites=t_cha_overwrites,
                                                category=team_category)

        await bot.guilds[0].create_voice_channel(name="Team Talk",
                                                 overwrites=t_cha_overwrites,
                                                 category=team_category)

        return team_role

    @staticmethod
    async def delete_team(bot: Bot, category: CategoryChannel) -> None:
        """deletes a team by the category"""
        await (get(bot.guilds[0].roles, name=category.name)).delete()

        for channel in category.channels:
            await channel.delete()
        await category.delete()


class RoleCog(Cog, name="RoleManager"):
    """is a cog with functions for creating, deleting and distributing roles"""

    contributor = [MikeCodes2586, AlbertUnruh]

    ext = Ext

    def __init__(self, bot: Bot):
        self.bot = bot

    # this is no longer in use since the Team 'll be created automatically
    '''
    @command(name="make_team")
    async def create_team(self, ctx: Context, *name: str):
        """creates a role, category, a text and a voice channel for a team and gives the author the role"""

        team_name = " ".join(name)
        users = DbUser.get_users(id=ctx.author.id)
        user = users[0] if len(users) else [None]*7
        if user[6] != team_name:
            embed: Embed = Embed(color=0x5865F2, title="Fehler")
            embed.add_field(name="Nicht in Team",
                            value=f"Melde dich in einem DM-Channel mit `{self.bot.user}` mit `{PREFIX}anmelden` an")
            await ctx.channel.send(embed=embed)
            return
        await self.ext.create_team(self.bot, team_name, ctx.author)
    '''

    @command(name="remove_team", aliases=["remove"])
    async def remove_team(self, ctx: Context,
                          category: Optional[CategoryChannel] = None):
        """deletes a category with the channels inside"""
        if category is None:
            await ctx.channel.send(
                f"Bitte gebe einen richtigen Teamnamen an!\n"
                f"Achte auf Großschreibung\n"
                f"Nutzung: `{PREFIX}remove_team [dein team name]` (in \" \" wenn er Leerzeichen hat)")
            return

        # Admins had to join a Team to delete it
        '''
        users = User.get_users(id=ctx.author.id)
        user = users[0] if len(users) else [None]*7
        if user[6] != category.name:
            embed: Embed = Embed(color=0x5865F2, title="Fehler")
            embed.add_field(name="Nicht in Team",
                            value=f"Melde dich in einem DM-Channel mit `{self.bot.user}` mit `{PREFIX}anmelden` an")
            await ctx.channel.send(embed=embed)
            return
        '''

        if not self.bot.guilds[0].get_member(ctx.author.id).guild_permissions.manage_roles:
            await ctx.channel.send("Du hast nicht genug perms!")
            return

        if not DbUser.get_users(team=category.name):
            await ctx.channel.send("Hey! Warum willst du das löschen?\n"
                                   "Das ist gar kein Team... \\:(")
            return

        for user in DbUser.get_users(team=category.name):
            DbUser.delete_user(id=user[0])

        await self.ext.delete_team(self.bot, category)

    # this is no longer in use since the Teams are managed by the `CheckinCog`
    '''
    @command(name="join_team", aliases=["join"])
    async def give_author_role(self, ctx: Context,
                               role: Optional[Role] = None):
        """gives the author the selected role"""

        user = DbUser.get_users(id=ctx.author.id)[0]
        if user[6] != role.name:
            embed: Embed = Embed(color=0x5865F2, title="Fehler")
            embed.add_field(name="Nicht in Team",
                            value=f"Melde dich in einem DM-Channel mit `{self.bot.user}` mit `{PREFIX}anmelden` an")
            await ctx.channel.send(embed=embed)
            return

        # ctx.author can also be a User...
        await self.bot.guilds[0].get_member(ctx.author.id).add_roles(role)

        await ctx.channel.send("Es hat funtioniert!")

    @command(name="exit_team", aliases=["leave", "exit"])
    async def remove_author_role(self, ctx: Context,
                                 role: Optional[Role] = None):
        """removes the author the selected role"""

        if role is None:
            embed: Embed = Embed(color=0x5865F2, title="Fehler")
            embed.add_field(name="Kein Argument",
                            value="Du hast kein (gültiges) Team angegeben")
            await ctx.channel.send(embed=embed)
            return

        # ctx.author can also be a User...
        await self.bot.guilds[0].get_member(ctx.author.id).remove_roles(role)

        await ctx.channel.send("Es hat funtioniert!")
    '''

    @command(name="check_team", aliases=["check"])
    async def check_for_team_in_db(self, ctx: Context,
                                   *name: str):
        """checks if the given team is in the database"""

        team_name = "".join(VALID_CHARS.findall(" ".join(name)))
        team = DbUser.get_users(team=team_name)

        if not team:
            await ctx.channel.send(
                f"Das Team gibt es nicht (achte auf Großschreibung).\n"
                f"Du kannst ein Team mit `{PREFIX}make_team mein teamname`(Leerzeichen möglich) erstellen wenn du die `manage_roles` permission hast.")
            return
        await ctx.channel.send(f"Das Team existiert und hat {len(team)} Mitglied(er)")
