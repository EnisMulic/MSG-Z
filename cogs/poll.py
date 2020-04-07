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

def setup(client):
    client.add_cog(Poll(client))