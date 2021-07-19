import discord
from discord.ext import commands

from constants import channels
from utils import checks


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @checks.in_channel(channels.BOT_COMMANDS, channels.LOGGER)
    async def invite(self, ctx):
        """Create a one time use invite"""

        channel_lobby = discord.utils.get(ctx.guild.text_channels, name=channels.LOBBY)
        
        invite_link = await channel_lobby.create_invite(max_uses = 1, unique = True, reason = f"Created by {ctx.author.display_name}")

        channel_dm = await ctx.author.create_dm()
        await channel_dm.send(invite_link)


def setup(bot):
    bot.add_cog(Misc(bot))
