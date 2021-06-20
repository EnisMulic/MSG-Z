from discord.ext import commands

from . import errors

def in_channel(*channels):
    def predicate(ctx):
        return ctx.message.channel.name in channels
    return commands.check(predicate)

def doesnt_have_any_role(*roles):
    def predicate(ctx):
        for role in ctx.author.roles:
            if role.name in roles:
                raise errors.HasForbiddenRole('You have a role that prevents you from using this command')
        return True
    return commands.check(predicate)