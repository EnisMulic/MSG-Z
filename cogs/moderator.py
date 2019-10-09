import discord
from discord.ext import commands

import datetime
from cogs import database #database.py

from cogs.utils import logger


class Moderator(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["add-role"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_role(self, ctx, member: discord.Member, *roles: discord.Role):#test this
        newRolesList = []
        for role in roles:
            newRole = discord.utils.get(member.guild.roles, name=str(role))
            if newRole not in member.roles:
                newRolesList += [newRole.mention]
                await member.add_roles(newRole)
            else:
                await ctx.send(member.nick + ' vec ima ulogu ' + newRole.name)
        
        
        
    @commands.command(aliases=["remove-role"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_role(self, ctx, member: discord.Member, *roles: discord.Role):
        for role in roles:
            oldRole = discord.utils.get(member.guild.roles, name=str(role))
            if oldRole in member.roles:
                await member.remove_roles(oldRole)   
            else:
                await ctx.send(member.nick + ' nema ulogu ' + oldRole.name)
        
        
    @commands.command(aliases=["set-name"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_name(self, ctx, member: discord.Member, *nick):
        newName = ' '.join(nick)
        await member.edit(nick = newName)
            
    
    #new cog ???
    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def purge(self, ctx, numberOfMessages = 1):
        await ctx.channel.purge(limit = int(numberOfMessages + 1))
        #log
        
        
       
def setup(client):
    client.add_cog(Moderator(client))