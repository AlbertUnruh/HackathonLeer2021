"""contains the Cog for the GitHub connection"""
from discord.ext.commands import Bot, Cog
from discord import TextChannel, PermissionOverwrite, Embed
from json import load, dump
from contributor import AlbertUnruh


class GithubCog(Cog, name="Github"):
    """is a Cog for the GitHub connection"""

    contributor = [AlbertUnruh]

    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def add(self):
        """checks if a channel for GitHub exits, otherwise it 'll be created"""
        if "GITHUB" not in self.get_channel_ids_json():
            channel: TextChannel = await self.bot.guilds[0].create_text_channel(
                name="github",
                overwrites={
                    self.bot.guilds[0].default_role: PermissionOverwrite(**{
                        "send_messages": False
                    })
                }
            )
            embed: Embed = Embed(color=0x5865F2, title="GitHub",
                                 description="""\
Hier ist ein [Tutorial](https://www.youtube.com/watch?v=RdifjyEuUbE), \
um einen Webhook zu erstellen und diesen mit GitHub zu verknüpfen.

(Dieser Channel kann gerne verschoben werden und diese Nachricht kann auch \
gelöscht werden, sobald alles fertig eingerichtet ist.)
""")
            data = self.get_channel_ids_json()
            data["GITHUB"] = channel.id
            with open("./CHANNEL_IDS.json", "w") as f:
                dump(data, f, indent=2)

            await channel.send(embed=embed)

    @staticmethod
    def get_channel_ids_json() -> dict:
        """returns the ids from the json-file"""
        with open("./CHANNEL_IDS.json") as f:
            return load(f)
