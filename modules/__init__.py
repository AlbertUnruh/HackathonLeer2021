"""registers all commands for the Bot automatically when the function
`register_commands` is called"""
from discord.ext.commands import Bot
from importlib import import_module
from os import listdir


cogs = [c.split(".")[0] for c in listdir(__name__) if not c.startswith("_")]


def register_commands(bot: Bot) -> None:
    """registers all commands"""
    for cog in cogs:
        bot.add_cog(import_module(f".{cog}", __package__).
                    __getattribute__(f"{cog.title()}Cog")(bot))
