import discord
from discord.ext import commands

import datetime

from constants import roles
from utils import logger


class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        role = discord.utils.get(member.guild.roles, name = roles.NEREGISTROVAN)
        await member.add_roles(role)

        embed = discord.Embed(title = "Member Joined", colour = discord.Colour.green())
        embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Created", value=member.created_at.replace(microsecond=0).isoformat(' '), inline=True)
        embed.add_field(name="Joined", value=member.joined_at.replace(microsecond=0).isoformat(' '), inline=True)
        embed.set_thumbnail(url = member.avatar_url)

        await logger.log_action(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        embed = discord.Embed(title = "Member Left", colour = discord.Colour.red())
        embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)
        embed.add_field(name="User", value=member.mention, inline=False)
        embed.add_field(name="Created", value=member.created_at.replace(microsecond=0).isoformat(' '), inline=True)
        embed.add_field(name="Joined", value=member.joined_at.replace(microsecond=0).isoformat(' '), inline=True)
        embed.add_field(name="Left", value=datetime.datetime.now().replace(microsecond=0).isoformat(' '), inline=True)
        embed.set_thumbnail(url = member.avatar_url)

        await logger.log_action(member.guild, embed)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # Roles removed
        if before.roles < after.roles:
            role_set = set(before.roles) - set(after.roles)
            roles = [role.mention for role in role_set]

            embed = discord.Embed(
                title = 'Role removed',
                colour = discord.Colour.green(),
                description = f"{' '.join(roles)} removed from {before.mention}"
            )
            embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)
                
            await logger.log_to_guild(self.bot, embed)
                   
        # Roles added
        elif before.roles > after.roles:
            role_set = set(after.roles) - set(before.roles)
            roles = [role.mention for role in role_set]

            embed = discord.Embed(
                title = 'Role added',
                colour = discord.Colour.green(),
                description = f"{' '.join(roles)} added to {before.mention}"
            )
            embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)
                
            await logger.log_to_guild(self.bot, embed)
 
        if before.nick != after.nick:
            embed = discord.Embed(
                title = "Name changed",
                colour = discord.Colour.green(),
                description = f"{before.mention} changed nickname from {before.nick} to {after.nick}"
            )
            embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)

            await logger.log_to_guild(self.bot, embed)

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.User, after: discord.User):
        if before.name != after.name:
            embed = discord.Embed(
                title = "User changed name",
                colour = discord.Colour.greyple(),
                description = f"{before.mention} changed username from {before.name} to {after.name}"
            )
            embed.set_author(name=before.display_name, url = before.avatar_url, icon_url = before.avatar_url)

            await logger.log_to_guild(self.bot, embed)

        if before.discriminator != after.discriminator:
            embed = discord.Embed(
                title = "User changed discriminator",
                colour = discord.Colour.greyple(),
                description = f"{before.mention} changed discriminator from {before.discriminator} to {after.discriminator}"
            )
            embed.set_author(name=before.display_name, url = before.avatar_url, icon_url = before.avatar_url)

            await logger.log_to_guild(self.bot, embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        embed = self._get_embed_message_deleted(message)
        await logger.log_action(message.guild, embed)

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, messages):
        for message in messages:
            embed = self._get_embed_message_deleted(message)
            await logger.log_action(message.guild, embed)

    def _get_embed_message_deleted(self, message):
        embed = discord.Embed(title = "Message deleted", description=message.content, colour = discord.Colour.red())
        embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)
        embed.set_thumbnail(url = message.author.avatar_url)
        embed.add_field(name = "Author", value = message.author.mention, inline = False)
        embed.add_field(name = "Channel", value = message.channel.mention, inline = False)
        embed.add_field(name = "Created", value = message.created_at.replace(microsecond=0).isoformat(' '), inline = True)
        embed.add_field(name = "Deleted", value = datetime.datetime.now().replace(microsecond=0).isoformat(' '), inline = True)

        return embed


def setup(bot):
    bot.add_cog(Event(bot))
