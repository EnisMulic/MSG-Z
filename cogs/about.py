import discord
from discord.ext import commands
from discord.ext import tasks

class About(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def source(self, ctx):
        """Get source code for this bot."""

        link = 'https://github.com/PancakeAlchemist/MSG-Z'
        await ctx.send(link)

    @commands.command(aliases=["man"])
    async def manual(self, ctx, cmd):
        """Get manual for command."""

        
        for cog in self.client.cogs:
            for command in self.client.get_cog(cog).walk_commands():
                if command.name == cmd or cmd in command.aliases:
                    cmds_desc = '$[' + ' | '.join(alias for alias in command.aliases) + '] ' + command.signature
                    cmds_desc = '```\n' + cmds_desc + '```'
                    await ctx.send(cmds_desc)      

def setup(client):
    client.add_cog(About(client))