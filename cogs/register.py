import discord
from discord.ext import commands
from discord.ext import tasks

class Register(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def register(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid git command passed...')

    @register.command()
    async def name(self, ctx, *, name):
        await ctx.send(f'Your name is {name}')

      

def setup(client):
    client.add_cog(Register(client))