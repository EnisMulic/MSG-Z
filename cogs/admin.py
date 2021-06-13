from discord.ext import commands

from constants import roles

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR)
    async def load(self, ctx, extension):
        self.bot.load_extension(f"cogs.{extension}")

        await ctx.send(f"Successfully loaded the {extension} module :thumbsup: ")

    @load.error
    async def load_error(self, ctx, error):
        await ctx.send(f"The following error occured:```\n{error}\n```")

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR)
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f"cogs.{extension}")

        await ctx.send(f"Successfully unloaded the {extension} module :thumbsup: ")

    @unload.error
    async def unload_error(self, ctx, error):
        await ctx.send(f"The following error occured:```\n{error}\n```")

def setup(bot):
    bot.add_cog(Admin(bot))