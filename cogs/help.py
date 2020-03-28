import discord
from discord.ext import commands
from discord.ext import tasks

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(add_reactions=True, embed_links=True)
    async def help(self, ctx, *, search_cog = None):
        """Gets all cogs and commands of this bot."""

        
        helpEmbed = discord.Embed(
            title='Cog Listing',
            description='Use `$help *cog*` to find out more about them!\n(The Cog Name Must Be in Title Case, Just Like this Sentence.)'
        )
        

        cogs = [cog for cog in self.client.cogs if cog == search_cog] if search_cog is not None else [cog for cog in self.client.cogs]
        
        for cog in cogs:
            cmds_desc = ''
            for command in self.client.get_cog(cog).walk_commands():
                cmds_desc += f"{command.name} - {command.help}\n"
            
            if cmds_desc is not '':
                helpEmbed.add_field(name = cog, value = cmds_desc, inline=False)
                

        await ctx.send(embed = helpEmbed)

def setup(client):
    client.add_cog(Help(client))