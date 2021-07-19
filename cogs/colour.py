import discord
from discord.ext import commands

import random


class Colour(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["clr", "color"])
    async def colour(self, ctx, hex):
        """Convert hex code to colour."""

        hex = hex.strip("#")
        url = f"https://dummyimage.com/900x900/{hex}/{hex}"
        
        embed = discord.Embed(
            title = "Colour",
            description = "#" + hex
        )
        
        embed.set_thumbnail(url = url)
        await ctx.reply(embed = embed)

    def _rand(self):
        random.randint(0, 255)

    @commands.command(aliases=["randclr", "rand-clr", "rand-colour", "rand-color"])
    async def rand_colour(self, ctx):
        """Get random colour."""

        hex = '{:02x}{:02x}{:02x}'.format(self._rand(), self._rand(), self._rand())
        url = f"https://dummyimage.com/900x900/{hex}/{hex}"
        
        embed = discord.Embed(
            title = "Colour",
            description = "#" + hex
        )

        embed.set_thumbnail(url = url)
        await ctx.reply(embed = embed)
                

def setup(bot):
    bot.add_cog(Colour(bot))
