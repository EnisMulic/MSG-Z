import discord
from discord.ext import commands

import datetime
# import database #database.py

from cogs.utils import logger
from cogs.utils import misc

class ModeratorUser(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["set-index"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_index(self, ctx, member: discord.Member, userIndex):
        database = self.client.get_cog('Database')
        if database is not None:
            await database.InsertUser(ctx, member, userIndex)

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
            
    
    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def kick(self, ctx, member: discord.Member, reason = None):
        await member.kick(reason = reason)
        action = discord.Embed(
            title = "User kicked",
            colour = discord.Colour.red().value
        )

        action.add_field(
            name = "Member: ",
            value = member.mention + ' ' + member.name + '#' + member.discriminator,
            inline = False
        )

        action.add_field(
            name = "Reason:",
            value = reason,
            inline = False
        )

        action.add_field(
            name = "Performed by:",
            value = ctx.author.mention,
            inline = False
        )

        action.set_thumbnail(url = member.avatar_url)

        await logger.LogAction(self.client, action)

    @commands.command()
    @commands.has_any_role('Administrator')
    async def ban(self, ctx, member: discord.Member, reason = None):
        await member.ban()
        
        action = discord.Embed(
            title = "Member banned",
            colour = discord.Colour.red().value
        )

        action.add_field(
            name = "Member:",
            value = member.mention + ' ' + member.name + '#' + member.discriminator,
            inline = False
        )

        action.add_field(
            name = "Reason:",
            value = reason,
            inline = False
        )

        action.add_field(
            name = "Performed by:",
            value = ctx.author.mention,
            inline = False
        )

        action.set_thumbnail(url = member.avatar_url)

        await logger.LogAction(self.client, action)


def setup(client):
    client.add_cog(ModeratorUser(client))