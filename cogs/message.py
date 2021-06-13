import discord
from discord.ext import commands

from constants import roles
from utils import logger

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = "Delete N last messages")
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def purge(self, ctx, number_of_messages = 1):
        """Delete n number of messages in a channel"""

        await ctx.channel.purge(limit = int(number_of_messages + 1))
        embed = discord.Embed(
            colour = discord.Colour.red(),
            description = str(number_of_messages) + " messages deleted in " + ctx.message.channel.mention,
        )

        embed.set_author(name = ctx.author.nick, icon_url = ctx.author.avatar_url)

        await logger.log_action(ctx.guild, embed)

    @commands.command(aliases=["msg-echo"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def echo(self, ctx, channel: discord.TextChannel, *, message = None):
        """Send message to a channel as the bot"""

        files = []
        for attachment in ctx.message.attachments:
            files.append(await attachment.to_file())
        await channel.send(content = message, files = files)

    @commands.command(aliases=["msg-publish"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def publish(self, ctx, channel: discord.TextChannel, *, message = None):
        """Send message to a channel as the bot and publish it"""
        
        files = []
        for attachment in ctx.message.attachments:
            files.append(await attachment.to_file())
        message = await channel.send(content = message, files = files)
        await message.publish()

    @commands.command(aliases=["msg-edit"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def edit(self, ctx, channel: discord.TextChannel, id: int, *, new_message):
        """Edit message sent as the bot"""

        message = await channel.fetch_message(id)
        await message.edit(content = new_message)

def setup(bot):
    bot.add_cog(Message(bot))