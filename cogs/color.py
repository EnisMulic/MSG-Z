import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import aiohttp

import random

class Color(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def color(self, ctx, hex):
        """Get random color."""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.thecolorapi.com/id?hex={hex}') as response:

                embed = discord.Embed(
                    title = "Color",
                    description = hex
                )   

                data = await response.json()
                embed.set_thumbnail(url = "http://www.thecolorapi.com/id?format=svg&hex=HEX%7D")
                await ctx.send(embed = embed)

    @commands.command()
    async def rand_color(self, ctx):
        r = lambda: random.randint(0,255)
        hex = '#{:02x}{:02x}{:02x}'.format(r(), r(), r())

        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.thecolorapi.com/id?hex={hex}') as response:

                embed = discord.Embed(
                    title = "Color",
                    description = hex
                )   

                data = await response.json()
                embed.set_thumbnail(url = "http://www.thecolorapi.com/id?format=svg&hex=HEX%7D")
                await ctx.send(embed = embed)

def setup(client):
    client.add_cog(Color(client))