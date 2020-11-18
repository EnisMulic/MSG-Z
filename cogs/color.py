import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import aiohttp

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

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
                
                
                drawing = svg2rlg(data["image"]["named"])
                renderPM.drawToFile(drawing, "image.png", fmt="PNG")
                embed.set_thumbnail(url = "./image.png")
                await ctx.send(embed = embed)
      

def setup(client):
    client.add_cog(Color(client))