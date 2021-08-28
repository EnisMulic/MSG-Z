from discord.ext import commands


class HasForbiddenRole(commands.CheckFailure):
    pass


class NotInDateTimeRange(commands.CheckFailure):
    pass
