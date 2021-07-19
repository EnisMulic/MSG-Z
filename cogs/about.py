from discord.ext import commands


class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def source(self, ctx):
        """Get source code for this bot."""
        
        await ctx.send('https://github.com/EnisMulic/MSG-Z')


def setup(bot):
    bot.add_cog(About(bot))
