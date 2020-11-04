import discord
from discord.ext import commands

import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import datetime

from models.user import User
from models.role import Role
from models.user import users_roles_association
import models.base as base

from utils import logger
from utils import misc

class ModeratorUser(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = base.Session()

    @commands.command(aliases=["add-member", "am"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_member(self, ctx, member: discord.Member, user_index):
        try:
            member_nick = member.nick if member.nick is not None else member.name

            new_user = User(
                member.id, user_index, member_nick, 
                member.name, member.discriminator
            )
            self.session.add(new_user)
            self.session.commit()
                            
            await ctx.send("Member added")
        except SQLAlchemyError as err:
            await ctx.send(str(err))
            self.session.rollback()

    @commands.command(aliases=["remove-account", "remove-acc"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_account(self, ctx, user_index):
        try:
            account = self.session.query(User) \
                .filter(User.UserIndex == user_index) \
                .one()
            
            self.session.delete(account)
            self.session.commit()

            await ctx.send("Account removed")
        except SQLAlchemyError as err:
            await ctx.send(str(err))
            self.session.rollback()

    @commands.command(aliases=["change-account", "change-acc"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def change_account(self, ctx, old_account: discord.Member, new_account: discord.Member):
        try:
            account = self.session.query(User) \
                .filter(User.UserId == old_account.id) \
                .one()
            
            if account is not None:
                account.UserId = new_account.id
                await old_account.kick()
                
            self.session.commit()

            await ctx.send("Account changed")
        except SQLAlchemyError as err:
            await ctx.send(str(err))
            self.session.rollback()

    @commands.command(aliases=["set-index"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_index(self, ctx, member: discord.Member, user_index: str):
        try:
            user = self.session.query(User) \
                .filter(User.UserId == member.id) \
                .one()
            
            user.UserIndex = user_index
            self.session.commit()
            
            await ctx.send("Index set")
        except SQLAlchemyError as err:
            await ctx.send(str(err))

         
    @commands.command(aliases=["add-role"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_role(self, ctx, member: discord.Member, *roles: discord.Role):
        new_roles = []
        for role in roles:
            new_role = discord.utils.get(member.guild.roles, name=str(role))
            if new_role not in member.roles:
                new_roles += [new_role.mention]
                await member.add_roles(new_role)
                # event.py triggered
            else:
                await ctx.send(member.nick + ' vec ima ulogu ' + new_role.name)
        
        
        
    @commands.command(aliases=["remove-role"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_role(self, ctx, member: discord.Member, *roles: discord.Role):
        for role in roles:
            old_role = discord.utils.get(member.guild.roles, name=str(role))
            if old_role in member.roles:
                await member.remove_roles(old_role) 
                # event.py triggered
            else:
                await ctx.send(member.nick + ' nema ulogu ' + old_role.name)
        
        
    @commands.command(aliases=["set-name"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_name(self, ctx, member: discord.Member, *name: str):
        new_name = ' '.join(name)
        await member.edit(nick = new_name)
        # event.py triggered
        await ctx.send("Name set")
            
    
    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def kick(self, ctx, member: discord.Member, reason = None):
        await member.kick(reason = reason)
        action = discord.Embed(
            title = "User kicked",
            colour = discord.Colour.red()
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

        try: 
            user = self.session.query(User)\
                .filter(User.UserId == member.id)\
                .one()
                
            user.StatusDiscord = "Kicked"    
            self.session.commit()    
                
        except SQLAlchemyError as err:    
            await ctx.send(str(err))    

    @commands.command()
    @commands.has_any_role('Administrator')
    async def ban(self, ctx, member: discord.Member, reason = None):
        await member.ban()
        
        action = discord.Embed(
            title = "Member banned",
            colour = discord.Colour.red()
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

        try:
            user = self.session.query(User) \
                .filter(User.UserId == member.id) \
                .one()
            
            user.StatusDiscord = "Banned"
            self.session.commit()
                
        except SQLAlchemyError as err:
            await ctx.send(str(err))
            

    @commands.command()
    async def revoke(self, ctx):
        try:
            user_roles = self.session.query(User, users_roles_association) \
                .filter(User.UserId == ctx.author.id) \
                .filter(users_roles_association.c.UserId == ctx.author.id)
            
            guild = self.client.get_guild(440055845552914433)
            user = guild.get_member(ctx.author.id)

            for user_role in user_roles:
                new_role = misc.getRoleById(self.client, user_role.RoleId)
                if new_role.id != 440055845552914433:
                    await user.add_roles(new_role)

            removeRole = misc.getRoleByName(self.client, "Neregistrovan(a)")
            await user.remove_roles(removeRole)
            self.session.commit()
            
            
            await user.edit(nick = user_roles[0].User.Name)
            self.session.commit()
        
        except SQLAlchemyError as err:
            await ctx.send(str(err))

    @commands.command()
    async def mute(self, ctx, member: discord.Member = None):
        muteRole = misc.getRoleByName(self.client, "Muted")

        if member is None:
            member = ctx.author

        await member.add_roles(muteRole)


def setup(client):
    client.add_cog(ModeratorUser(client))