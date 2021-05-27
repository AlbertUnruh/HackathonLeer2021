from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext.commands import Bot
from discord.ext import ipc
import WEBCONFIG
from database import DbUser
from modules.countdown import CountdownCog
from contributor import RedstoneCraft
from typing import Optional

contributor = [RedstoneCraft]
### from datenbank-utils import sqlite-kram
app = Quart(__name__, template_folder="templates")
ipc_client = ipc.Client(secret_key=WEBCONFIG.SECRET_KEY)

app.config["DISCORD_CLIENT_ID"] = WEBCONFIG.DISCORD_CLIENT_ID
app.config["DISCORD_CLIENT_SECRET"] = WEBCONFIG.DISCORD_CLIENT_SECRET
app.config["DISCORD_BOT_TOKEN"] = WEBCONFIG.DISCORD_BOT_TOKEN
app.config["DISCORD_REDIRECT_URI"] = WEBCONFIG.DISCORD_CLIENT_ID

discord = DiscordOAuth2Session(app)

bot: Optional[Bot] = None


def run(bot_: Bot = None, host: str = "0.0.0.0", port: int = 8080):
    """runs the dashboard"""
    global bot
    bot = bot_
    app.run(host, port)


#################### DASHBOARD ####################

@app.route("/")
async def home():
    termins = await CountdownCog(bot).get_timestamps()
    await render_template("index.html", termins=termins)


@app.route("/login/")
async def login():
    return await discord.create_session()


@app.route("/callback/")
async def callback():
    try:
        return discord.callback()
    except:
        return url_for("login")


@app.route("/dashboard/")
async def dashboard():
    authorized = await discord.authorized
    if authorized is not True:
        return redirect(url_for("login"))
    user = await discord.fetch_user()
    user_name = ipc_client.request("get_display_name_by_id",
                                   user_id=user.id)
    users = DbUser.get_all_users()
    return render_template("dashboard.html", users=users)
