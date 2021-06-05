import discord
from discord.ext import commands

import random

class Color(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["clr"])
    async def color(self, ctx, hex):
        """Get random color."""
        hex = hex.strip("#")
        url = f"https://dummyimage.com/900x900/{hex}/{hex}"
        
        embed = discord.Embed(
            title = "Color",
            description = "#" + hex
        )  
        

        embed.set_thumbnail(url = url)
        await ctx.send(embed = embed)

    @commands.command(aliases=["randclr"])
    async def rand_color(self, ctx):
        r = lambda: random.randint(0,255)
        hex = '{:02x}{:02x}{:02x}'.format(r(), r(), r())
        url = f"https://dummyimage.com/900x900/{hex}/{hex}"
        
        embed = discord.Embed(
            title = "Color",
            description = "#" + hex
        )  

        embed.set_thumbnail(url = url)
        await ctx.send(embed = embed)
                

def setup(client):
    client.add_cog(Color(client))