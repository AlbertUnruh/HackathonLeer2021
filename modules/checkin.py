"""this is to check in new users"""
from discord.ext.commands import Bot, Cog, command, Context, CommandError
from discord import Embed, Reaction, User, DMChannel
from contributor import AlbertUnruh
from re import compile
from database import User as DbUser
from colorama import Fore as Fg, Style


VALID_CHARS = compile(r"[a-zA-Z0-9_.+\- @äöü]")
VALID_MAIL = compile(r"(^[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
TITLE = "__**Anmeldung\u200B:**__"
YES, NO = "✅", "❌"

EMAIL = "E-Mail"
NAME = "Name"
SCHOOL = "Schule"
CLASS = "Klasse"
TEAM = "Team"


def escape_input(string: str) -> str:
    """escapes user input to prevent SQL-injections"""
    return "".join(VALID_CHARS.findall(string))


async def check_in_error(self, ctx: Context, error: CommandError):
    """if the user has done great sh*t"""
    await ctx.send("Bitte gebe alles an!\n`"
                   "\"E-MAIL\" "
                   "\"DEIN NAME\" "
                   "\"DEINE SCHULE\" "
                   "\"DEINE KLASSE\" "
                   "\"DEIN TEAM\"`")


class CheckinCog(Cog, name="Checkin"):
    """is a Cog for the check in for new users"""

    contributor = [AlbertUnruh]

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="anmelden", aliases=["anmeldung"])
    async def check_in(self, ctx: Context, mail: str, name: str,
                       school: str, cl4ss: str, team: str):
        """checks a new user in"""

        # if the message wasn't send on in the direct/private chat
        if ctx.guild is not None:
            await ctx.message.delete()
            await ctx.send(f"**__Bitte nutze mich nur im Privat-Chat"
                           f"{ctx.author.mention}!__**")
            return

        # if the mail is invalid
        if not VALID_MAIL.match(mail):
            await ctx.send("Bitte gebe eine gültige E-Mail an!")
            return

        embed: Embed = Embed(title=TITLE, description=f"""\
Bitte gehe sicher, dass alle Angaben korrekt sind.
_Wenn die stimmen, drücke _\\{YES}_, ansonsten _\\{NO}_._
""")
        embed.add_field(name=EMAIL, value=escape_input(mail))
        embed.add_field(name=NAME, value=escape_input(name))
        embed.add_field(name=SCHOOL, value=escape_input(school))
        embed.add_field(name=CLASS, value=escape_input(cl4ss))
        embed.add_field(name=TEAM, value=escape_input(team))

        msg = await ctx.send(embed=embed)
        await msg.add_reaction(YES)
        await msg.add_reaction(NO)

    check_in.on_error = check_in_error

    @Cog.listener("on_reaction_add")
    async def validates(self, reaction: Reaction, user: User):
        """inserts the user into the DB, if `YES` was reacted"""

        # if the bot has added the reaction
        if user == self.bot.user:
            return

        # if the reaction was made on a server
        if not isinstance(reaction.message.channel, DMChannel):
            return

        # if a invalid reaction was added
        if reaction.emoji not in (YES, NO):
            return

        # if there is no embed on the message
        if len(reaction.message.embeds) != 1:
            return

        # if the user cancels the check in
        if reaction.emoji == NO:
            await reaction.message.delete()
            return

        embed: Embed = reaction.message.embeds[0]

        # if the title is invalid
        if embed.title != TITLE:
            return

        attrs = {}
        for field in embed.fields:
            attrs[field.name] = field.value

        user_data = {
            "id": user.id,
            "user": user.name,
            "mail": attrs.get(EMAIL),
            "name": attrs.get(NAME),
            "school": attrs.get(SCHOOL),
            "cl4ss": attrs.get(CLASS),
            "team": attrs.get(TEAM)
        }
        DbUser.new_user(**user_data)
        print(Fg.MAGENTA+f"Added new user to the DB! {user_data}"+Style.RESET_ALL)
