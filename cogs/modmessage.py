import discord
from discord.ext import commands

import datetime

from models.post import Post
from models.user import User
import models.base as base

from utils import logger



class ModeratorMsg(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = base.Session()

    @commands.command(description = "Delete N last messages")
    @commands.has_any_role('Administrator', 'Moderator')
    async def purge(self, ctx, number_of_messages = 1):
        """Delete n number of messages in a channel"""

        await ctx.channel.purge(limit = int(number_of_messages + 1))
        action = discord.Embed(
            colour = discord.Colour.red(),
            description = str(number_of_messages) + " messages deleted in " + ctx.message.channel.mention,
        )
        action.set_author(
            name = ctx.author.nick,
            icon_url = ctx.author.avatar_url
        )
        
        
        await logger.LogAction(self.client, action)

    @commands.command(aliases=["msg-echo"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def echo(self, ctx, channel, *, message = None):
        """Send message to a channel as the bot"""

        channel_id = int(channel[2:len(channel) - 1])
        message_channel = self.client.get_channel(channel_id)
        
        
        files = []
        for attachment in ctx.message.attachments:
            files.append(await attachment.to_file())
        await message_channel.send(content = message, files = files)
        
        try:
            user = self.session.query(User) \
                .filter(User.UserId == ctx.author.id) \
                .one()

            newPost = Post(message_channel.last_message_id, message_channel.id, user)
            self.session.add(newPost)
            self.session.commit()
        except Exception as err:
            await ctx.send(str(err))


    @commands.command(aliases=["msg-edit"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def edit(self, ctx, channel, id: int, *, new_message):
        """Edit message sent as the bot"""

        message_channel = self.client.get_channel(int(channel[2:len(channel) - 1]))
        message = await message_channel.fetch_message(id)
        await message.edit(content = new_message)

        try:
            post = self.session.query(Post) \
                .filter(Post.PostId == id) \
                .one()
            
            post.UserId = ctx.author.id
            self.session.commit()
        except Exception as err:
            await ctx.send(str(err))
            

    @commands.command(aliases=["msg-move"], 
                      description = "Move a message from one channel to another\
                                     \n\nOption: \n -d or --delete = delete message after move")
    @commands.has_any_role('Administrator', 'Moderator')
    async def move(self, ctx, old_channel, id: int, new_channel, option = None):
        """Move a message from one channel to another"""
        
        if option != None and option != '--delete' and option != '-d':
            return

        old_channel_id = int(old_channel[2:len(old_channel) - 1])
        from_channel = self.client.get_channel(old_channel_id)
        message = await from_channel.fetch_message(id)
        message_embed = discord.Embed(
            colour = discord.Colour.blue(),
            image = message.author.avatar_url
        )

        message_embed.add_field(
            name = "Autor: ",
            value = message.author.mention,
            inline = False
        )
        
        message_embed.add_field(
            name = "Poruka: ",
            value = message.content,
            inline = False
        )

        message_embed.add_field(
            name = "Vrijeme: ",
            value = str(message.created_at.strftime("%d %B %Y %H:%M:%S")),
            inline = False
        )

        message_embed.add_field(
            name = "Iz: ",
            value = from_channel.mention,
            inline = False
        )

        new_channel_id = int(new_channel[2:len(new_channel) - 1])
        to_channel = self.client.get_channel(new_channel_id)
        
        if option == '--delete' or option == '-d':
            await message.delete()

        await to_channel.send(embed = message_embed)


def setup(client):
    client.add_cog(ModeratorMsg(client))