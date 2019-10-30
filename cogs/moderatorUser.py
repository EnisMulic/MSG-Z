import discord
from discord.ext import commands

import datetime

from utils import logger

class ModeratorUser(commands.Cog):
    def __init__(self, client):
        self.client = client

        print(self.client.guilds)

    @commands.command(aliases=["add-member"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_member(self, ctx, member: discord.Member, userIndex):
        database = self.client.get_cog('Database')
        if database is not None:
            await database.insert_member(ctx, member, userIndex)

    @commands.command(aliases=["set-index"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_index(self, ctx, member: discord.Member, userIndex: str):
        database = self.client.get_cog('Database')
        if database is not None:
            await database.change_member_index(ctx, member, userIndex.upper())

    @commands.command(aliases=["set-status"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_status(self, ctx, member: discord.Member, status, option):
        if option == '-f':
            database = self.client.get_cog('Database')
            if database is not None:
                await database.change_member_fakultet_status(ctx, member, status)
        elif option == '-d':
            database = self.client.get_cog('Database')
            if database is not None:
                await database.change_member_discord_status(ctx, member, status)
            


    @commands.command(aliases=["add-role"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_role(self, ctx, member: discord.Member, *roles: discord.Role):
        database = self.client.get_cog('Database')

        newRolesList = []
        for role in roles:
            newRole = discord.utils.get(member.guild.roles, name=str(role))
            if newRole not in member.roles:
                newRolesList += [newRole.mention]
                await member.add_roles(newRole)
                if database is not None:
                    await database.insert_users_role(member, newRole)
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
    async def set_name(self, ctx, member: discord.Member, *name: str):
        newName = ' '.join(name)
        await member.edit(nick = newName)
        database = self.client.get_cog('Database')
        if database is not None:
            await database.change_member_name(member, newName)
            
    
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

        database = self.client.get_cog('Database')
        if database is not None:
            await database.change_member_discord_status(ctx, member, "Kicked")

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

        database = self.client.get_cog('Database')
        if database is not None:
            await database.change_member_discord_status(ctx, member, "Banned")

        
def setup(client):
    client.add_cog(ModeratorUser(client))