import discord
from discord.ext import commands

from models import poll, poll_option

class Poll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["create-poll", "add-poll"], description = "Create a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def create_poll(self, ctx, *, name: str):
        name = name.strip('\"')
        
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                new_poll = poll.Poll(name, None, None, ctx.author.id)

                session.add(new_poll)
                session.commit()
            except Exception as err:
                await ctx.send(str(err))
            finally:
                session.close()

    @commands.command(aliases=["add-option"], description = "Add option to a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_option(self, ctx, name, icon, text):
        name = name.strip('\"')
        text = text.strip('\"')

        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()

                poll_search = session.query(poll.Poll) \
                    .filter(poll.Poll.Name == name) \
                    .one()

                if poll_search is not None:
                    new_poll_option = poll_option.PollOption(icon, text, poll_search)
                    session.add(new_poll_option)
                    session.commit()

                    if poll_search.MessageId is not None and poll_search.ChannelId is not None:
                        await self.update_poll(name, session, poll_search.ChannelId, poll_search.MessageId)
            except Exception as err:
                await ctx.send(str(err))
            finally:
                session.close()
    
    @commands.command(aliases=["remove-option"], description = "Remove option from a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_option(self, ctx, name, icon):
        name = name.strip('\"')

        database = self.client.get_cog("Database")
        if database is not None:
            try:
                session = database.Session()
                poll_search = session.query(poll.Poll) \
                                .filter(poll.Poll.Name == name) \
                                .one()
                
                if poll_search is not None:
                    poll_option_search = session.query(poll_option.PollOption) \
                                    .filter(poll.Poll.PollId == poll_search.PollId) \
                                    .filter(poll_option.PollOption.Icon == icon) \
                                    .one()

                    session.delete(poll_option_search)
                    session.commit()

                    await ctx.send(icon + " removed")

                    if poll_search.MessageId is not None and poll_search.ChannelId is not None:
                        await self.update_poll(name, session, poll_search.ChannelId, poll_search.MessageId)

            except Exception as err:
                await ctx.send(str(err))
            finally:
                session.close()

    @commands.command(aliases=["edit-icon"], description = "Edit option emoji in a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def edit_option_icon(self, ctx, name, old_icon, new_icon):
        name = name.strip('\"')

        database = self.client.get_cog("Database")
        if database is not None:
            try:
                session = database.Session()
                poll_search = session.query(poll.Poll) \
                                .filter(poll.Poll.Name == name) \
                                .one()
                
                if poll_search is not None:
                    poll_option_search = session.query(poll_option.PollOption) \
                                    .filter(poll.Poll.PollId == poll_search.PollId) \
                                    .filter(poll_option.PollOption.Icon == old_icon) \
                                    .one()

                    poll_option_search.Icon = new_icon
                    session.commit()

                    
                    if poll_search.MessageId is not None and poll_search.ChannelId is not None:
                        await self.update_poll(name, session, poll_search.ChannelId, poll_search.MessageId)

            except Exception as err:
                await ctx.send(str(err))
            finally:
                session.close()

    @commands.command(aliases=["edit-option"], description = "Edit option in a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def edit_option_text(self, ctx, name, icon, *, new_text):
        name = name.strip('\"')

        database = self.client.get_cog("Database")
        if database is not None:
            try:
                session = database.Session()
                poll_search = session.query(poll.Poll) \
                                .filter(poll.Poll.Name == name) \
                                .one()
                
                if poll_search is not None:
                    poll_option_search = session.query(poll_option.PollOption) \
                                    .filter(poll.Poll.PollId == poll_search.PollId) \
                                    .filter(poll_option.PollOption.Icon == icon) \
                                    .one()

                    poll_option_search.Text = new_text
                    session.commit()

                    if poll_search.MessageId is not None and poll_search.ChannelId is not None:
                        await self.update_poll(name, session, poll_search.ChannelId, poll_search.MessageId)

            except Exception as err:
                await ctx.send(str(err))
            finally:
                session.close()

    @commands.command(description = "Edit option emoji in a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def poll(self, ctx, channel, *, name):
        name = name.strip('\"')
        channel_id = int(channel[2:len(channel) - 1])
        message_channel = self.client.get_channel(channel_id)

        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()
            embed = await self.build_poll(session, name)
            
            message = await ctx.send(embed = embed)

            poll_search = session.query(poll.Poll) \
                            .filter(poll.Poll.Name == name) \
                            .one()
            
            poll_search.ChannelId = channel_id
            poll_search.MessageId = message.id
            session.commit()
            session.close()
            

    #build poll before posting or editing
    async def build_poll(self, session, name):
        name = name.strip('\"')
        try:
            poll_search = session.query(poll.Poll) \
                                .filter(poll.Poll.Name == name) \
                                .one()
                
            if poll_search is not None:
                poll_option_search = session.query(poll_option.PollOption) \
                                .filter(poll_option.PollOption.PollId == poll_search.PollId) \
                                .all()

                options = ""
                for poll_build_option in poll_option_search:
                    options += poll_build_option.Icon + " " + poll_build_option.Text + "\n\n"

                embed = discord.Embed(
                    title = poll_search.Name,
                    description = options
                )

                return embed
        except Exception as err:
            print(str(err))
    
    async def update_poll(self, name, session, channel_id, message_id):
        name = name.strip('\"')
        
        embed = await self.build_poll(session, name)
        message_channel = self.client.get_channel(channel_id)
        message = await message_channel.fetch_message(message_id)
        
        await message.edit(embed = embed)

def setup(client):
    client.add_cog(Poll(client))