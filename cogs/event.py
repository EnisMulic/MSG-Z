import discord
from discord.ext import commands

import datetime

from constants import roles
from utils import logger

class Events(commands.Cog):
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
        pass

    @commands.Cog.listener()
    async def on_user_update(self, before: discord.Member, after: discord.Member):
        pass

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
    bot.add_cog(Events(bot))