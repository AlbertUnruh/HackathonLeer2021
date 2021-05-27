from quart import Quart, render_template, request, session, redirect, url_for, 
import WEBCONFIG
from database import User
from modules.countdown import CountdownCog
from contributor import RedstoneCraft

contributor = [RedstoneCraft]
### from datenbank-utils import sqlite-kram
app = Quart(__name__, template_folder="templates")

#################### DASHBOARD ####################

@app.route("/")
async def home():
    users = User.get_all_users()
    await render_template("index.html", user = users)

@app.route("/login/")
async def login():
    return render_template("login.html")

@app.route("/dashboard/")
async def dashboard():
    if request.method == "POST":
        form = request.form
        if WEBCONFIG.PASSWORD != form["password"]:
            return(url_for("login"))
        else:
            return render_template("dashboard.html")

app.run(host = 1234, port = 1234)
