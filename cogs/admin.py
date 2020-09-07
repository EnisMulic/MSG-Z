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

    @commands.command()
    @commands.has_any_role('Administrator')
    async def lock(self, ctx, channel = None):
        if channel is None:
            channel = ctx.channel
        else:
            channel_id = int(channel[2:len(channel) - 1])
            channel = self.client.get_channel(channel_id)
        
        for role in channel.changed_roles:
            if role.name != "@everyone":
                await channel.set_permissions(
                    role, send_messages = False
                )

    @commands.command()
    @commands.has_any_role('Administrator')
    async def unlock(self, ctx, channel = None):
        if channel is None:
            channel = ctx.channel
        else:
            channel_id = int(channel[2:len(channel) - 1])
            channel = self.client.get_channel(channel_id)
        
        for role in channel.changed_roles:
            if role.name != "@everyone":
                await channel.set_permissions(
                    role, send_messages = True
                )

    @commands.command(aliases=["full-lock", "f-lock"])
    @commands.has_any_role('Administrator')
    async def full_lock(self, ctx, channel = None):
        if channel is None:
            channel = ctx.channel
        else:
            channel_id = int(channel[2:len(channel) - 1])
            channel = self.client.get_channel(channel_id)
        
        for role in channel.changed_roles:
            await channel.set_permissions(
                role, read_messages = False
            )
                  

    @commands.command(aliases=["full-unlock", "f-unlock"])
    @commands.has_any_role('Administrator')
    async def full_unlock(self, ctx, channel = None):
        if channel is None:
            channel = ctx.channel
        else:
            channel_id = int(channel[2:len(channel) - 1])
            channel = self.client.get_channel(channel_id)
        
        for role in channel.changed_roles:
            if role.name != "@everyone":
                await channel.set_permissions(
                    role, read_messages = True
                )    

def setup(client):
    client.add_cog(Administrator(client))