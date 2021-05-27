"""this is to check in new users"""
from discord.ext.commands import Bot, Cog, command, Context, CommandError
from discord import Embed, Reaction, Role, Member, User, DMChannel
from discord.utils import get
from contributor import AlbertUnruh
from re import compile
from database import DbUser as DbUser
from colorama import Fore as Fg, Style
from CONFIGS import PREFIX, BLACKLISTED_ROLES, BLACKLISTED_MSG

from .role import Ext


VALID_CHARS = compile(r"[a-zA-Z0-9_.+\- @äöü]")
VALID_MAIL = compile(r"(^[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
TITLE_NEW = "__**Anmeldung\u200B:**__"
TITLE_DEL = "__**Datenlöschung\u200B:**__"
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

        if DbUser.get_users(id=ctx.author.id):
            await ctx.send(f"**Hey, du bist schon angemeldet, bitte mache `"
                           f"{PREFIX}abmelden` um dich danach mit neuen "
                           f"Daten anmelden zu können!**")
            return

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

        # if the role is blacklisted
        if escape_input(team).replace("@", "") in BLACKLISTED_ROLES:
            await ctx.send(BLACKLISTED_MSG.format(role=team))
            return

        embed: Embed = Embed(title=TITLE_NEW, description=f"""\
Bitte gehe sicher, dass alle Angaben korrekt sind.
_Wenn die stimmen, drücke _\\{YES}_, ansonsten _\\{NO}_._
""")
        embed.add_field(name=EMAIL, value=escape_input(mail))
        embed.add_field(name=NAME, value=escape_input(name))
        embed.add_field(name=SCHOOL, value=escape_input(school))
        embed.add_field(name=CLASS, value=escape_input(cl4ss))
        embed.add_field(name=TEAM, value=escape_input(team).replace("@", ""))

        msg = await ctx.send(embed=embed)
        await msg.add_reaction(YES)
        await msg.add_reaction(NO)

    check_in.on_error = check_in_error

    @command(name="abmelden", aliases=["abmeldung"])
    async def check_out(self, ctx: Context):
        """checks a user out"""

        if not DbUser.get_users(id=ctx.author.id):
            await ctx.send(f"**Hey, du bist nicht angemeldet, bitte mache `"
                           f"{PREFIX}anmelden` um dich anzumelden!**")
            return

        embed: Embed = Embed(title=TITLE_DEL, description=f"""\
Bitte bestätige mit \\{YES}, dass du dich abmelden möchtest.
**WARNUNG: DIESE AKTION KANN NICHT RÜCKGÄNGIG GEMACHT WERDEN!**
""")

        msg = await ctx.author.send(embed=embed)
        await msg.add_reaction(YES)

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

        if embed.title == TITLE_NEW:
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

            member: Member = self.bot.guilds[0].get_member(user.id)

            role: Role = await Ext.create_team(self.bot, user_data["team"], member)
            await member.add_roles(role)
            await user.send(f"Du wurdest dem Team `{user_data['team']}` hinzugefügt!")

            await reaction.message.delete()
            return

        if embed.title == TITLE_DEL:
            users = DbUser.get_users(id=user.id)
            if not len(users):
                return
            user_ = users[0]

            DbUser.delete_user(id=user.id)
            print(Fg.MAGENTA+f"Removed user {user} from the DB!"+Style.RESET_ALL)

            role: Role = get(self.bot.guilds[0].roles, name=user_[6])
            await self.bot.guilds[0].get_member(user.id).remove_roles(role)
            await user.send("Du hast dich soeben abgemeldet.\n"
                            "Ich wünsche dir noch einen schönen Tag oder Abend oder was auch immer \\:)")

            if not DbUser.get_users(team=role.name):
                await Ext.delete_team(self.bot, get(self.bot.guilds[0].categories, name=role.name))
                await user.send("Das Team wurde automatisch gelöscht, da es keine Mitglieder mehr hatte!")

            await reaction.message.delete()
            return
