import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import aiohttp

class Color(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def color(self, ctx, hex = None):
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
      

def setup(client):
    client.add_cog(Color(client))