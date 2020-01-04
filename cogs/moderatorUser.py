import discord
from discord.ext import commands

import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import datetime

from models.user import User
from models.role import Role

from utils import logger

class ModeratorUser(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["add-member"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_member(self, ctx, member: discord.Member, userIndex):
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                memberNick = member.nick if member.nick is not None else member.name
                session = database.Session()
                newUser = User(
                    member.id, userIndex, memberNick, 
                    member.name, member.discriminator, 
                    "Aktivan", "Aktivan"
                )
                session.add(newUser)
                session.commit()
                session.close()
                # await database.insert_member(ctx, member, userIndex)
                await ctx.send("Member added")
            except SQLAlchemyError as err:
                await ctx.send(str(err))

    @commands.command(aliases=["set-index"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_index(self, ctx, member: discord.Member, userIndex: str):
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                user = session.query(User) \
                            .filter(User.UserId == member.id) \
                            .one()
                user.UserIndex = userIndex
                session.commit()
                # await database.change_member_index(ctx, member, userIndex.upper())
                session.close()
                await ctx.send("Index set")
            except SQLAlchemyError as err:
                await ctx.send(str(err))

    @commands.command(aliases=["set-status"], description = "Option:\n\t -d = Discord \n\t -f = Fakultet")
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_status(self, ctx, member: discord.Member, status, option):
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                user = session.query(User) \
                        .filter(User.UserId == member.id) \
                        .one()
                

                if option == '-f':
                    user.StatusFakultet = status
                    session.commit()
                    await ctx.send("FakultetStatus set")    
                elif option == '-d':
                    user.StatusDiscord = status
                    session.commit()
                    await ctx.send("DiscordStatus set") 
                
                session.close()
            except SQLAlchemyError as err:
                await ctx.send(str(err))
            
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
                # event.py triggered
            else:
                await ctx.send(member.nick + ' vec ima ulogu ' + newRole.name)
        
        
        
    @commands.command(aliases=["remove-role"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_role(self, ctx, member: discord.Member, *roles: discord.Role):
        database = self.client.get_cog('Database')

        for role in roles:
            oldRole = discord.utils.get(member.guild.roles, name=str(role))
            if oldRole in member.roles:
                await member.remove_roles(oldRole) 
                # event.py triggered
            else:
                await ctx.send(member.nick + ' nema ulogu ' + oldRole.name)
        
        
    @commands.command(aliases=["set-name"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_name(self, ctx, member: discord.Member, *name: str):
        newName = ' '.join(name)
        await member.edit(nick = newName)
        # event.py triggered
        await ctx.send("Name set")
            
    
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
            try:
                session = database.Session()
                user = session.query(User) \
                        .filter(User.UserId == member.id) \
                        .one()
                
                user.StatusDiscord = "Kicked"
                session.commit()
                session.close()
            except SQLAlchemyError as err:
                await ctx.send(str(err))

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
            try:
                session = database.Session()
                user = session.query(User) \
                        .filter(User.UserId == member.id) \
                        .one()
                
                user.StatusDiscord = "Discord"
                session.commit()
                session.close()
            except SQLAlchemyError as err:
                await ctx.send(str(err))

            await database.change_member_discord_status(ctx, member, "Banned")

        
def setup(client):
    client.add_cog(ModeratorUser(client))