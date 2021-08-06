from typing import Literal
from discord.ext import commands

from datetime import date, datetime

from . import errors


def in_channel(*channels):
    def predicate(ctx):
        return ctx.message.channel.name in channels
    return commands.check(predicate)


def doesnt_have_any_role(*roles):
    def predicate(ctx) -> Literal[True]:
        for role in ctx.author.roles:
            if role.name in roles:
                raise errors.HasForbiddenRole('You have a role that prevents you from using this command')
        return True
    return commands.check(predicate)


def in_date_range(start: date, stop: date):
    def suffix(d):
        return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

    def custom_strftime(format, t):
        return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

    def predicate(ctx):
        now = datetime.now()
        if (now.day < start.day and now.month < start.month) or (now.day > stop.day and now.month > stop.month):
            start_date_formated = custom_strftime('%B {S}', start)
            stop_date_formated = custom_strftime('%B {S}', stop)
            raise errors.NotInDateTimeRange(f'This command can only be used from {start_date_formated} to {stop_date_formated}')
        return True
    return commands.check(predicate)
