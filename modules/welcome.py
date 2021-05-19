from discord.ext.commands import Bot, Cog
from CHANNEL_IDS import WELCOME
from contributor import MikeCodes2586

w_channel = client.get_channel(WELCOME)

class WelcomeCog(Cog, name="Welcome"):
  """ is a Cog for welcoming new users """

  contributor = [MikeCodes2586]

  def __init__(self, bot: Bot):
    self.bot = bot

  @Cog.listener()
  async def on_member_join(member):
    await w_channel.send(f'Welcome to the server {member.mention}!')
