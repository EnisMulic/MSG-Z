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
    async def add_option(self, ctx, name, text, icon):
        name = name.strip('\"')
        text = text.strip('\"')

        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()

                search_poll = session.query(poll.Poll) \
                    .filter(poll.Poll.Name == name) \
                    .one()

                if search_poll is not None:
                    new_poll_option = poll_option.PollOption(icon, text, search_poll)
                    session.add(new_poll_option)
                    session.commit()

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
            except Exception as err:
                await ctx.send(str(err))

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
            except Exception as err:
                await ctx.send(str(err))

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
                                    .filter(poll_option.PollOption.Icon == old_icon) \
                                    .one()

                    poll_option_search.Text = new_text
                    session.commit()
            except Exception as err:
                await ctx.send(str(err))

    @commands.command(description = "Edit option emoji in a poll")
    @commands.has_any_role('Administrator', 'Moderator')
    async def poll(self, ctx, channel, *, name):
        channel_id = int(channel[2:len(channel) - 1])
        message_channel = self.client.get_channel(channel_id)

    #build poll before posting or editing
    async def build_poll(self, session, name):
        try:
            poll_build = session.query(poll.Poll, poll_option.PollOption) \
                            .filter(poll.Poll.Name == name) \
                            .one()

        except Exception as err:
            print(str(err))

def setup(client):
    client.add_cog(Poll(client))