import discord
from discord.ext import commands
from discord.ext import tasks

class About(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def source(self, ctx):
        """Get source code for this bot."""

        link = 'https://github.com/PancakeAlchemist/MSG-Z'
        await ctx.send(link)

def setup(client):
    client.add_cog(About(client))