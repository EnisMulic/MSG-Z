import discord
from discord.ext import commands

import datetime
# import database #database.py

from cogs.utils import logger
from cogs.utils import misc

class ModeratorMsg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def purge(self, ctx, numberOfMessages = 1):

        await ctx.channel.purge(limit = int(numberOfMessages + 1))
        action = discord.Embed(
            title = "Message(s) deleted",
            colour = discord.Colour.red().value
        )

        action.add_field(
            name = "Action performed by: ",
            value = ctx.author.mention,
            inline = False
        )

        action.add_field(
            name = "Channel:",
            value = ctx.message.channel.mention,
            inline = False
        )

        action.add_field(
            name = "Number of messages:",
            value = numberOfMessages,
            inline = False
        )

        await logger.LogAction(self.client, action)

    @commands.command(aliases=["msg-echo"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def echo(self, ctx, channel, *, message):
        messageChannel = self.client.get_channel(int(channel[2:len(channel) - 1]))
        await messageChannel.send(message)
        print(messageChannel.last_message_id)  #for database


    @commands.command(aliases=["msg-edit"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def edit(self, ctx, channel, id: int, *, newMessage):
        messageChannel = self.client.get_channel(int(channel[2:len(channel) - 1]))
        message = await messageChannel.fetch_message(id)
        await message.edit(content = newMessage)

    @commands.command(aliases=["msg-move"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def move(self, ctx, oldChannel, id: int, newChannel, option = None):

        if option != None and option != '--delete' and option != '--d':
            return

        fromChannel = self.client.get_channel(int(oldChannel[2:len(oldChannel) - 1]))
        message = await fromChannel.fetch_message(id)
        messageEmbed = discord.Embed(
            colour = discord.Colour.blue().value,
            image = message.author.avatar_url
        )

        messageEmbed.add_field(
            name = "Autor: ",
            value = message.author.mention,
            inline = False
        )
        
        messageEmbed.add_field(
            name = "Poruka: ",
            value = message.content,
            inline = False
        )

        messageEmbed.add_field(
            name = "Vrijeme: ",
            value = str(message.created_at.strftime("%d %B %Y %H:%M:%S")),
            inline = False
        )

        messageEmbed.add_field(
            name = "Iz: ",
            value = fromChannel.mention,
            inline = False
        )

        toChannel = self.client.get_channel(int(newChannel[2:len(newChannel) - 1]))
        
        if option == '--delete' or option == '--d':
            await message.delete()

        await toChannel.send(embed = messageEmbed)


def setup(client):
    client.add_cog(ModeratorMsg(client))