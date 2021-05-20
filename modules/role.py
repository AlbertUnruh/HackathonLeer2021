"""contains cog for role functions"""
from discord.ext.commands import Bot, Cog, Context, command
from discord import Role, CategoryChannel, PermissionOverwrite
from discord.utils import get
from typing import Optional
from contributor import MikeCodes2586


class RoleCog(Cog, name="RoleManager"):
    """is a cog with funtions for creating, deleting and destributing roles"""

    # TODO: @make_team @remove_team @give_role
    # add perm check
    # add account check

    contributor = [MikeCodes2586]

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="make_team")
    async def create_team(self, ctx: Context, *name: str):
        """creates a role, category, a text and a voice channel for a team and gives the author the role"""
        team_name = " ".join(name)
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
            return

        await (get(self.bot.guilds[0].roles, name=category.name)).delete()

        for channel in category.channels:
            await channel.delete()
        await category.delete()

    @command(name="give_role")
    async def give_author_role(self, ctx: Context,
                              role: Optional[Role] = None):
        """gives the author the selected role"""

        # role = get(self.bot.guilds[0].roles, name=category.name)
        await self.bot.guilds[0].get_member(ctx.author.id).add_roles(role)

