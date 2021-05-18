from discord.ext.commands import Bot, Cog
from discord import VoiceChannel, TextChannel, PermissionOverwrite, Message
from datetime import datetime, timedelta
from asyncio import sleep as asleep
from typing import Tuple, List, Optional
from json import load, dump


class CountdownCog(Cog, name="Countdown"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @Cog.listener("on_ready")
    async def countdown(self):
        # syncs on the `5th` minute
        # this action can take up to 10 minutes to avoid rate-limiting
        minute = datetime.utcnow().minute % 5 + 5
        await asleep((60*minute)-datetime.utcnow().second)
        del minute

        while True:
            stamp, event = await self.next_timestamp()
            channel_id = self.get_channel_ids_json().get("COUNTDOWN", None)
            if channel_id is None:
                channel = await self.create_channel_voice()
            else:
                channel: VoiceChannel = self.bot.guilds[0].get_channel(channel_id)
                if channel is None:
                    channel = await self.create_channel_voice()

            await channel.edit(name=f"{event} {self.convert_stamp(stamp)}")

            # the are no longer used in the code
            # and 'll be assigned later again
            del channel, channel_id, event, stamp

            # the frequency is every 5 minutes because of rate-limiting
            # ..note::
            #   the `utcnow`-call is to sync on full minutes
            await asleep((60*5)-datetime.utcnow().second)

    async def next_timestamp(self) -> Tuple[datetime, str]:
        """gets the next timestamp for the countdown"""
        channel_id = self.get_channel_ids_json().get("CONFIG COUNTDOWN", None)
        if channel_id is None:
            channel = await self.create_channel_text()
        else:
            channel: TextChannel = self.bot.guilds[0].get_channel(channel_id)
            if channel is None:
                channel = await self.create_channel_text()

        message: Message
        msgs: List[Message] = []
        async for message in channel.history(limit=None):
            if message.author == self.bot.user:
                continue
            msgs.append(message)

        newest: Tuple[Optional[datetime], str] = (None, "...")
        for message in msgs:
            try:
                name, stamp = message.content.splitlines(keepends=False)
                stamp = datetime.fromisoformat(stamp)
            except ValueError:
                pass
            else:
                if newest[0] is None:
                    newest = (stamp, name)
                elif newest[0] > stamp > datetime.utcnow():
                    newest = (stamp, name)
        return newest if newest[0] is not None else (datetime.utcnow(), "...")

    @staticmethod
    def convert_stamp(stamp: datetime) -> str:
        """converts the stamp for the countdown"""
        dif: timedelta = stamp-datetime.utcnow()
        if dif.total_seconds() < 0:
            return "00:00:00"
        ret = list()

        ret.append(f"{dif.days:0>2}")
        ret.append(f"{dif.seconds // 3600:0>2}")
        ret.append(f"{dif.seconds % 3600 // 60:0>2}")

        return ":".join(ret)

    async def create_channel_voice(self) -> VoiceChannel:
        """creates a new channel for the countdown"""
        channel: VoiceChannel = await self.bot.guilds[0].create_voice_channel(
            name="initialising countdown...",
            overwrites={
                self.bot.guilds[0].default_role: PermissionOverwrite(**{
                    "connect": False
                })
            }
        )
        data = self.get_channel_ids_json()
        data["COUNTDOWN"] = channel.id
        with open("./CHANNEL_IDS.json", "w") as f:
            dump(data, f, indent=2)
        return channel

    async def create_channel_text(self) -> TextChannel:
        """creates a new channel for the countdown configs"""
        channel: TextChannel = await self.bot.guilds[0].create_text_channel(
            name="events - countdown config",
            overwrites={
                self.bot.guilds[0].default_role: PermissionOverwrite(**{
                    "view_channel": False,
                    "send_messages": False
                })
            }
        )
        data = self.get_channel_ids_json()
        data["CONFIG COUNTDOWN"] = channel.id
        with open("./CHANNEL_IDS.json", "w") as f:
            dump(data, f, indent=2)
        await channel.send("""\
Hier werden die Events eingetragen, bitte nutzen Sie folgende Syntax für die Events:
```
NAME DES EVENTS
ZEITSTEMPEL IM ISOFORMAT IN UTC
```        
""")
        return channel

    @staticmethod
    def get_channel_ids_json() -> dict:
        with open("./CHANNEL_IDS.json") as f:
            return load(f)
