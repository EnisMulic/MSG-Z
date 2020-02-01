import discord
from discord.ext import commands

import datetime

from models.post import Post
from models.user import User

from utils import logger



class ModeratorMsg(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description = "Delete N last messages")
    @commands.has_any_role('Administrator', 'Moderator')
    async def purge(self, ctx, numberOfMessages = 1):

        await ctx.channel.purge(limit = int(numberOfMessages + 1))
        action = discord.Embed(
            title = "Message(s) deleted",
            colour = discord.Colour.red()
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

    @commands.command(aliases=["msg-echo"], description = "Send message to a channel as the bot")
    @commands.has_any_role('Administrator', 'Moderator')
    async def echo(self, ctx, channel, *, message = None):
        messageChannel = self.client.get_channel(int(channel[2:len(channel) - 1]))
        
        
        files = []
        for attachment in ctx.message.attachments:
            files.append(await attachment.to_file())
        await messageChannel.send(content = message, files = files)
        
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()
            user = session.query(User) \
                    .filter(User.UserId == ctx.author.id) \
                    .one()

            newPost = Post(messageChannel.last_message_id, messageChannel.id, user)
            session.add(newPost)
            session.commit()
            session.close()
        


    @commands.command(aliases=["msg-edit"], description = "Edit message sent as the bot")
    @commands.has_any_role('Administrator', 'Moderator')
    async def edit(self, ctx, channel, id: int, *, newMessage):
        messageChannel = self.client.get_channel(int(channel[2:len(channel) - 1]))
        message = await messageChannel.fetch_message(id)
        await message.edit(content = newMessage)

        database = self.client.get_cog('Database')
        if database is not None:
            post = database.session.query(Post) \
                        .filter(Post.PostId == id) \
                        .one()
            post.UserId = ctx.author.id
            database.session.commit()

    @commands.command(aliases=["msg-move"], 
                      description = "Move a message from one channel to another\
                                     \n\nOption: \n -d or --delete = delete message after move")
    @commands.has_any_role('Administrator', 'Moderator')
    async def move(self, ctx, oldChannel, id: int, newChannel, option = None):

        if option != None and option != '--delete' and option != '-d':
            return

        fromChannel = self.client.get_channel(int(oldChannel[2:len(oldChannel) - 1]))
        message = await fromChannel.fetch_message(id)
        messageEmbed = discord.Embed(
            colour = discord.Colour.blue(),
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
        
        if option == '--delete' or option == '-d':
            await message.delete()

        await toChannel.send(embed = messageEmbed)


def setup(client):
    client.add_cog(ModeratorMsg(client))