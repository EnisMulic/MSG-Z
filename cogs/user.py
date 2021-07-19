import discord
from discord.ext import commands

from constants import roles
from utils import logger


class User(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["add-role", "add-roles"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def add_role(self, ctx, member: discord.Member, *roles: discord.Role):
        """Add roles to member"""

        for role in roles:
            if role not in member.roles:
                await member.add_roles(role)

    @commands.command(aliases=["remove-role", "remove-roles"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def remove_role(self, ctx, member: discord.Member, *roles: discord.Role):
        """Remove roles from member"""

        for role in roles:
            if role in member.roles:
                await member.remove_roles(role)

    @commands.command(aliases=["set-name"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def set_name(self, ctx, member: discord.Member, *, name: str):
        """Edit members display name"""

        await member.edit(nick = name)

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def kick(self, ctx, member: discord.Member, reason = None):
        """Kick member"""

        await member.kick(reason = reason)
        embed = discord.Embed(
            title = "Member kicked",
            colour = discord.Colour.red(),
            desciption = f'{member.mention} kicked out by {ctx.author.mention} - {reason}'
        )

        embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)

        await logger.log_action(ctx.guild, embed)

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def ban(self, ctx, member: discord.Member, reason = None):
        """Ban member"""

        await member.ban()

        embed = discord.Embed(
            title = "Member banned",
            colour = discord.Colour.red(),
            desciption = f'{member.mention} kicked out by {ctx.author.mention} - {reason}'
        )

        embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)

        await logger.log_action(ctx.guild, embed)

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def mute(self, ctx, member: discord.Member):
        """Add Muted role to member"""

        mute_role = discord.utils.get(ctx.guild.roles, name=roles.MUTED)
        await member.add_roles(mute_role)

    @commands.command(aliases=["mute+"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def mute_plus(self, ctx, member: discord.Member):
        """Add Muted+ role to member"""

        mute_role = discord.utils.get(ctx.guild.roles, name=roles.MUTED_PLUS)
        await member.add_roles(mute_role)

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def unmute(self, ctx, member: discord.Member):
        """Remove Muted role from member"""

        mute_role = discord.utils.get(ctx.guild.roles, name=roles.MUTED)
        await member.remove_roles(mute_role)

    @commands.command(aliases=["unmute+"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def unmute_plus(self, ctx, member: discord.Member):
        """Remove Muted+ role from member"""

        mute_role = discord.utils.get(ctx.guild.roles, name=roles.MUTED_PLUS)
        await member.remove_roles(mute_role)


def setup(bot):
    bot.add_cog(User(bot))
