import discord
from discord.ext import commands

import os

from models import poll, poll_option
import models.base as base

class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = base.Session()

    @commands.command(aliases=["create-poll", "add-poll"], description = "Create a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def create_poll(self, ctx, *, name: str):
        name = name.strip('\"')
        
        try:
            new_poll = poll.Poll(name, None, None, ctx.author.id)

            self.session.add(new_poll)
            self.session.commit()
        except Exception as err:
            await ctx.send(str(err))

    @commands.command(aliases=["add-option"], description = "Add option to a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_option(self, ctx, name, icon, text):
        name = name.strip('\"')
        text = text.strip('\"')

        try:
            poll_search = self.session.query(poll.Poll) \
                .filter(poll.Poll.Name == name) \
                .one()
            
            if poll_search is not None:
                new_poll_option = poll_option.PollOption(icon, text, poll_search)
                self.session.add(new_poll_option)
                self.session.commit()
        
                if poll_search.MessageId is not None and poll_search.ChannelId is not None:
                    await self.update_poll(name, poll_search.ChannelId, poll_search.MessageId)
        
        except Exception as err:
            await ctx.send(str(err))
    
    @commands.command(aliases=["remove-option"], description = "Remove option from a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_option(self, ctx, name, icon):
        name = name.strip('\"')

        try:
            poll_search = self.session.query(poll.Poll) \
                .filter(poll.Poll.Name == name) \
                .one()
            
            if poll_search is not None:
                poll_option_search = self.session.query(poll_option.PollOption) \
                    .filter(poll.Poll.PollId == poll_search.PollId) \
                    .filter(poll_option.PollOption.Icon == icon) \
                    .one()
        
                self.session.delete(poll_option_search)
                self.session.commit()
                await ctx.send(icon + " removed")
        
                if poll_search.MessageId is not None and poll_search.ChannelId is not None:
                    await self.update_poll(name, poll_search.ChannelId, poll_search.MessageId)
        
        except Exception as err:
            await ctx.send(str(err))

    @commands.command(aliases=["edit-icon"], description = "Edit option emoji in a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def edit_option_icon(self, ctx, name, old_icon, new_icon):
        name = name.strip('\"')

        try:
            poll_search = self.session.query(poll.Poll) \
                .filter(poll.Poll.Name == name) \
                .one()
            
            if poll_search is not None:
                poll_option_search = self.session.query(poll_option.PollOption) \
                    .filter(poll.Poll.PollId == poll_search.PollId) \
                    .filter(poll_option.PollOption.Icon == old_icon) \
                    .one()
                
                poll_option_search.Icon = new_icon
                self.session.commit()
                
                if poll_search.MessageId is not None and poll_search.ChannelId is not None:
                    await self.update_poll(name, poll_search.ChannelId, poll_search.MessageId)
        
        except Exception as err:
            await ctx.send(str(err))

    @commands.command(aliases=["edit-option"], description = "Edit option in a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def edit_option_text(self, ctx, name, icon, *, new_text):
        name = name.strip('\"')

        try:
            poll_search = self.session.query(poll.Poll) \
                .filter(poll.Poll.Name == name) \
                .one()
            
            if poll_search is not None:
                poll_option_search = self.session.query(poll_option.PollOption) \
                    .filter(poll.Poll.PollId == poll_search.PollId) \
                    .filter(poll_option.PollOption.Icon == icon) \
                    .one()
        
                poll_option_search.Text = new_text
                self.session.commit()
        
                if poll_search.MessageId is not None and poll_search.ChannelId is not None:
                    await self.update_poll(name, poll_search.ChannelId, poll_search.MessageId)
        
        except Exception as err:
            await ctx.send(str(err))

    @commands.command(description = "Edit option emoji in a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def poll(self, ctx, channel, *, name):
        """Post created poll to channel."""

        name = name.strip('\"')
        channel_id = int(channel[2:len(channel) - 1])
        message_channel = self.client.get_channel(channel_id)

        try:
            embed = await self.build_poll(name)
            
            message = await ctx.send(embed = embed)

            poll_search = self.session.query(poll.Poll) \
                .filter(poll.Poll.Name == name) \
                .one()
            
            poll_search.ChannelId = channel_id
            poll_search.MessageId = message.id
            
            self.session.commit()
            self.session.close()

            await self.add_reactions(name, message)
        except Exception as err:
            await ctx.send(str(err))

            
            

    #build poll before posting or editing
    async def build_poll(self, name):
        name = name.strip('\"')
        try:
            poll_search = self.session.query(poll.Poll) \
                .filter(poll.Poll.Name == name) \
                .one()
                
            if poll_search is not None:
                poll_option_search = self.session.query(poll_option.PollOption) \
                    .filter(poll_option.PollOption.PollId == poll_search.PollId) \
                    .all()

                embed = discord.Embed(title = poll_search.Name)
                embed.set_thumbnail(url = "https://www.shorturl.at/uwAB1")

                for poll_build_option in poll_option_search:
                    embed.add_field(
                        name = poll_build_option.Icon, 
                        value = poll_build_option.Text
                    )
                

                return embed
        except Exception as err:
            print(str(err))
    
    async def update_poll(self, name, channel_id, message_id):
        name = name.strip('\"')
        
        embed = await self.build_poll(name)
        message_channel = self.client.get_channel(channel_id)
        message = await message_channel.fetch_message(message_id)
        
        await message.edit(embed = embed)
        await self.add_reactions(name, message)

    async def add_reactions(self, name, message):
        poll_search = self.session.query(poll.Poll) \
            .filter(poll.Poll.Name == name) \
            .one()    


        reactions = self.session.query(poll_option.PollOption) \
            .filter(poll_option.PollOption.PollId == poll_search.PollId) \
            .all()

        reactions = [reaction.Icon for reaction in reactions]
        
        if reactions is not None:
            for reaction in reactions:
                await message.add_reaction(reaction)

            for reaction in message.reactions:
                if reaction.emoji not in reactions:
                    await message.clear_reaction(reaction)

def setup(client):
    client.add_cog(Poll(client))