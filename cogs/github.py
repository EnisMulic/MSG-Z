import discord
from discord.ext import commands
from discord.ext import tasks

class Github(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(description = "Get source code for this bot")
    async def source(self, ctx):
        link = 'https://github.com/PancakeAlchemist/MSG-Z'
        await ctx.send(link)

def setup(client):
    client.add_cog(Github(client))