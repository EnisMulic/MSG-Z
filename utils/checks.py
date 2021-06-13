from discord.ext import commands

def in_channel(*channels):
    def predicate(ctx):
        return ctx.message.channel.name in channels
    return commands.check(predicate)