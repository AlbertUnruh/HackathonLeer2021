"""contains the command error handler"""
from discord.ext.commands import Bot, Cog, Context, errors
from contributor import AlbertUnruh


class ErrorhandlerCog(Cog, name="Errorhandler"):
    """is the error handler for the bot"""

    contributor = [AlbertUnruh]

    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    @Cog.listener(name="on_command_error")
    async def handler(self, ctx: Context, error):
        """is the core from the handler"""

        # checks if the command has a own error handler
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            # originally from
            # `cog._get_overridden_method(cog.cog_command_error)`
            if getattr(cog.cog_command_error.__func__,
                       '__cog_special_method__', cog.cog_command_error
                       ) is not None:
                return

        ignored = (
            # if the prefix was entered, but no command could be found
            errors.CommandNotFound,

            # if a `"` or a `'` was used in a wrong syntax
            errors.InvalidEndOfQuotedStringError,
            errors.ExpectedClosingQuoteError,
            errors.UnexpectedQuoteError,

        )

        if isinstance(error, ignored):
            return

        # raises the error
        raise error
