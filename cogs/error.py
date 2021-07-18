import discord
from discord.ext import commands

import traceback
import sys

from utils import errors

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        
        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, 'original', error)

        # ignored = (commands.CommandNotFound, )
        # if isinstance(error, ignored):
        #     return
        
        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, commands.CommandNotFound):
            await ctx.reply(f'Command does not exist.')

        if isinstance(error, commands.DisabledCommand):
            await ctx.reply(f'Command has been disabled.')
        elif isinstance(error, errors.HasForbiddenRole):
            await ctx.reply(f'{str(error)}')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.reply(f'{str(error)}')
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.reply(f'Command can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        # elif isinstance(error, commands.BadArgument):
        #     if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
        #         await ctx.send('I could not find that member. Please try again.')

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))