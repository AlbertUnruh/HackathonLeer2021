from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc
import WEBCONFIG
from database import User
from modules.countdown import CountdownCog
from contributor import RedstoneCraft

contributor = [RedstoneCraft]
### from datenbank-utils import sqlite-kram
app = Quart(__name__, template_folder="templates")
ipc_client = ipc.Client(secret_key=WEBCONFIG.SECRET_KEY)

app.config["DISCORD_CLIENT_ID"] = WEBCONFIG.DISCORD_CLIENT_ID
app.config["DISCORD_CLIENT_SECRET"] = WEBCONFIG.DISCORD_CLIENT_SECRET
app.config["DISCORD_BOT_TOKEN"] = WEBCONFIG.DISCORD_BOT_TOKEN 
app.config["DISCORD_REDIRECT_URI"] = WEBCONFIG.DISCORD_CLIENT_ID

discord = DiscordOAuth2Session(app)

#################### DASHBOARD ####################

@app.route("/")
async def home():
    users = User.get_all_users()
    await render_template("index.html", user = users)

@app.route("/login/")
async def login():
    return await discord.create_session()

@app.route("/callback/")
async def callback():
    try:
        return discord.callback()
    except:
        return(url_for("login"))

@app.route("/dashboard/")
async def dashboard():
    authorized = await discord.authorized
    if authorized is not True:
        return redirect(url_for("login"))
    termins = await CountdownCog().get_timestamps()
    user = await discord.fetch_user()
    user_name = ipc_client.request("get_display_name_by_id", user_id=user["user_id"])
    #anmeldungs_formular = sqlite utils get_anmeldungen()
    return render_template("dashboard.html", termins = termins )

app.run(host = 1234, port = 1234)
