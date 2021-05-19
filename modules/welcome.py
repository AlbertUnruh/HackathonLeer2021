"""contains the welcoming Cog"""
from discord.ext.commands import Bot, Cog
from discord import TextChannel, Member, PermissionOverwrite
from json import load, dump
from contributor import MikeCodes2586


class WelcomeCog(Cog, name="Welcome"):
    """is a Cog for welcoming new users"""

    contributor = [MikeCodes2586]

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_member_join")
    async def send_welcome_msg(self, member: Member):
        """Sends welcome messages on join event"""
        channel_id = self.get_channel_ids_json().get("WELCOME", None)
        if channel_id is None:
            channel = await self.create_channel_welcome()
        else:
            channel: TextChannel = self.bot.guilds[0].get_channel(channel_id)
            if channel is None:
                channel = await self.create_channel_welcome()

        await channel.send(f'Wilkommen auf dem Server {member.mention}!')

    @staticmethod
    def get_channel_ids_json() -> dict:
        """returns the ids from the json-file"""
        with open("./CHANNEL_IDS.json") as f:
            return load(f)

    async def create_channel_welcome(self) -> TextChannel:
        """creates a new channel for welcome messages"""
        channel: TextChannel = await self.bot.guilds[0].create_text_channel(
            name="wilkommen",
            overwrites={
                self.bot.guilds[0].default_role: PermissionOverwrite(**{
                    "view_channel": True,
                    "send_messages": False
                })
            }
        )
        data = self.get_channel_ids_json()
        data["WELCOME"] = channel.id
        with open("./CHANNEL_IDS.json", "w") as f:
            dump(data, f, indent=2)

        return channel
