import discord
from discord.ext import commands

from utils import logger
from utils import misc

class Administrator(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_any_role('Administrator')
    async def load(self, ctx, extension):
        self.client.load_extension(f"cogs.{extension}")

        await ctx.send(f"Successfully loaded the {extension} module :thumbsup: ")

    @load.error
    async def load_error(self, ctx, error):
        await ctx.send(f"The following error occured:```\n{error}\n```")

    @commands.command()
    @commands.has_any_role('Administrator')
    async def unload(self, ctx, extension):
        self.client.unload_extension(f"cogs.{extension}")

        await ctx.send(f"Successfully unloaded the {extension} module :thumbsup: ")

    @unload.error
    async def unload_error(self, ctx, error):
        await ctx.send(f"The following error occured:```\n{error}\n```")


def setup(client):
    client.add_cog(Administrator(client))