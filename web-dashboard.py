from urllib.parse import urlencode
from quart import Quart, render_template, request, session, redirect, url_for
from quart_discord import DiscordOAuth2Session
from discord.ext import ipc
### from datenbank-utils import sqlite-kram
app = Quart(__name__, template_folder="templates", )
ipc_client = ipc.Client(secret_key="bsbq9r5!31!g§VHa8§v926Syp066E?3#6o1&5§!8")

app.config["DISCORD_CLIENT_ID"] = 843893717907406898
app.config["DISCORD_CLIENT_SECRET"] = "G_Ga5HSCD_Cpr0Z9vQePvIB81ZhoIZ_-"
app.config["DISCORD_BOT_TOKEN"] = "ODQzODkzNzE3OTA3NDA2ODk4.YKKfRQ.MHYJ9GK3uuDREXTEjtmabwRKHIs"     
app.config["DISCORD_REDIRECT_URL"] = ""

discord = DiscordOAuth2Session(app)

@app.route("/")
async def home():
    await render_template("index.html")

@app.route("/login/")
async def login():
    return await discord.create_session()

@app.route("/dashboard/")
async def dashboard():
    authorized = await discord.authorized
    if authorized is not True:
        return redirect(url_for("login"))
    
    user = await discord.fetch_user()
    user_name = ipc_client.request("get_display_name_by_id", user_id=user["user_id"])
    #anmeldungs_formular = sqlite utils get_anmeldungen()
    
    