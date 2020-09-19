import discord
from discord.ext import commands
from discord.ext import tasks

import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import datetime

from models.role import Role
from models.user import users_roles_association
from models.user import User
import models.base as base

from utils import misc
from utils import randemoji

def is_in_channel(ctx):
    return ctx.channel.name == 'bot-commands' or ctx.channel.name == 'logger'

class SortTree:
  def __init__(self, value):

    self.left = None
    self.value = value
    self.right = None

  def insert_val(self, value):
    if value.Value < self.value.Value:
       if self.left is None:
         self.left = SortTree(value)
       else:
         self.left.insert_val(value)
    else:
       if self.right is None:
         self.right = SortTree(value)
       else:
         self.right.insert_val(value)

def display(_node):
   return list(filter(None, [i for b in [display(_node.left) if isinstance(_node.left, SortTree) else [getattr(_node.left, 'value', None)], [_node.value], display(_node.right) if isinstance(_node.right, SortTree) else [getattr(_node.right, 'value', None)]] for i in b]))
    

class Rankup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.roleName = "Registrovan"
        self.role = None
        self.roles = None

        self.session = base.Session()

    def SetRole(self):
        if self.role is None:
            self.role = misc.getRoleByName(self.client, self.roleName)

    def SetValue(self, role: Role):
        try:
            if role.ParentRole is not None:
                parent = self.session.query(Role) \
                    .filter(Role.RoleId == role.ParentRole) \
                    .one()
                
                children = self.session.query(Role) \
                    .filter(Role.ParentRole == role.ParentRole) \
                    .count()

                role.Value = parent.Value + 1 + children * 0.1
            else:
                role.Value = 0
        except SQLAlchemyError as err:
            print(str(err))
        

            
    
    def formRoles(self):
        if self.roles is None:
            try:
                ranked_roles = self.session.query(Role) \
                        .filter(Role.ParentRole != None) \
                        .all()

                RoleTree = SortTree(ranked_roles[0])
                for ranked_role in ranked_roles[1:]:
                    RoleTree.insert_val(ranked_role)


                self.roles = display(RoleTree)
            except SQLAlchemyError as err:
                print(str(err))


    def getUsersRankedRoles(self, user):
        try:
            ranked_roles = self.session.query(Role) \
                    .join(users_roles_association) \
                    .filter(Role.ParentRole != None) \
                    .filter(users_roles_association.c.UserId == user.id) \
                    .all()

            return ranked_roles
        except SQLAlchemyError as err:
            print(str(err))
        

            

    
    @commands.command()
    @commands.has_any_role('Administrator') 
    async def connect(self, ctx, parentRole: discord.Role, childRole: discord.Role):
        """Connect two discord roles (child role and parent role)."""

        try:
            parent = self.session.query(Role) \
                .filter(Role.RoleId == parentRole.id) \
                .one_or_none()

            child = self.session.query(Role) \
                .filter(Role.RoleId == childRole.id) \
                .one_or_none()

            if parent is not None and child is not None:
                child.ParentRole = parent.RoleId
                self.SetValue(child)
                self.session.commit()

        except SQLAlchemyError as err:
            await ctx.send(str(err))


    
    @commands.command()
    @commands.check(is_in_channel) 
    @commands.has_any_role('Treća godina') 
    async def imatrikulant(self, ctx):
        self.SetRole()
        await ctx.author.add_roles(self.role)
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je imatrikulant :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
        

    
    @commands.command()
    @commands.has_any_role('Treća godina')
    @commands.check(is_in_channel) 
    async def apsolvent(self, ctx):
        self.SetRole()
        await ctx.author.add_roles(self.role)
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je apsolvent :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        

        await ctx.send(embed = embed)

    @commands.command(aliases=["apsolvent+"])
    @commands.has_any_role('Treća godina')
    @commands.check(is_in_channel) 
    async def apsolvent_(self, ctx):
        self.SetRole()
        await ctx.author.add_roles(self.role)

        druga_godina_role = misc.getRoleByName(self.client, "Druga godina*")
        await ctx.author.remove_roles(druga_godina_role)
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je apsolvent :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        

        await ctx.send(embed = embed)

    
    @commands.command(aliases=["diplomirao", "diplomirala"])
    @commands.has_any_role('Treća godina')
    @commands.check(is_in_channel)
    async def diploma(self, ctx):
        
        await ctx.author.kick(reason = "Diplomirao/Diplomirala")
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :mortar_board: " + ctx.author.mention + " je diplomirao/diplomirala :mortar_board:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    
    @commands.command(aliases=["alumni", "alumna"])
    @commands.has_any_role('Treća godina') 
    @commands.check(is_in_channel) 
    async def alum(self, ctx):
        
        alum_role = misc.getRoleByName(self.client, "Alumni")
        await ctx.author.add_roles(alum_role)
        ranked_roles = self.getUsersRankedRoles(ctx.author)

        for role in ctx.author.roles:
            for ranked_role in ranked_roles:
                if role.id == ranked_role.RoleId:
                    await ctx.author.remove_roles(role)

        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :mortar_board: " + ctx.author.mention + " je diplomirao/diplomirala :mortar_board:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
    
    
    @commands.command(aliases=["ocistio", "ocistila"])
    @commands.check(is_in_channel) 
    async def cista(self, ctx):
        self.SetRole()
        ranked_roles = self.getUsersRankedRoles(ctx.author)
        highestRole, nextRole = self.findNextRole(ranked_roles)
        
        for role in ctx.author.roles:
            for ranked_role in ranked_roles:
                if role.id == ranked_role.RoleId:
                    await ctx.author.remove_roles(role)

        nextRole = misc.getRoleById(self.client, nextRole.RoleId)
        await ctx.author.add_roles(nextRole)
        await ctx.author.add_roles(self.role)

        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je ocistio/ocistila :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    
    
    @commands.command()
    @commands.check(is_in_channel) 
    async def uslov(self, ctx):
        self.SetRole()
        ranked_roles = self.getUsersRankedRoles(ctx.author)
        
        highestRole, nextRole = self.findNextRole(ranked_roles)
        nextRole = misc.getRoleById(self.client, nextRole.RoleId)


        for role in ctx.author.roles:
            for ranked_role in ranked_roles:
                if role.id == ranked_role.RoleId and role.id != highestRole.RoleId:
                    await ctx.author.remove_roles(role)

        await ctx.author.add_roles(nextRole)
        await ctx.author.add_roles(self.role)

        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je ispunio/ispunila uslov :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
        

    @commands.command(aliases=["obnovio", "obnovila"])
    @commands.check(is_in_channel) 
    async def obnova(self, ctx):
        self.SetRole()
        await ctx.author.add_roles(self.role)
        
        emoji = randemoji.Get()
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = f"\n {emoji} {ctx.author.mention} se je obnovio/obnovila {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    
    @commands.command()
    @commands.check(is_in_channel) 
    async def kolizija(self, ctx):
        self.SetRole()

        
        ranked_roles = self.getUsersRankedRoles(ctx.author)
        highestRole, nextRole = self.findNextRoleKolizija(ranked_roles)
        
        kozizijaRole = misc.getRoleById(self.client, nextRole.RoleId)
        
        await ctx.author.add_roles(kozizijaRole)
        await ctx.author.add_roles(self.role)
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je upisao/upisala koliziju :tada:"
        )
        
        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        
        await ctx.send(embed = embed)

    
    @commands.command()
    @commands.check(is_in_channel) 
    async def ispis(self, ctx):
        await ctx.author.kick(reason = "Ispis")
        emoji = randemoji.Get()
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = f"\n {emoji} {ctx.author.mention} se ispisao/ispisala {emoji}"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    @commands.command()
    @commands.check(is_in_channel) 
    async def mahalusa(self, ctx):
        ranked_roles = self.getUsersRankedRoles(ctx.author)
        
        highestRole, nextRole = self.findNextRole(ranked_roles)
        lowerRole = misc.getRoleById(self.client, highestRole.ParentRole)
	    
        
        await ctx.author.remove_roles(lowerRole)
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :spy: " + ctx.author.mention + " mahala :spy:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    def findNextRole(self, roles: []):
        if self.roles is None:
            self.formRoles()
        
        tree = SortTree(roles[0])
        for role in roles[1:]:
            tree.insert_val(role)
        
        list = display(tree)
        for item in list[::-1]:
            for role in self.roles[::-1]:
                if item.RoleId == role.ParentRole and role.Value.is_integer():
                    return item, role
        
        return None

    def findNextRoleKolizija(self, roles: []):
        if self.roles is None:
            self.formRoles()
        
        tree = SortTree(roles[0])
        for role in roles[1:]:
            tree.insert_val(role)
        
        list = display(tree)
        for item in list[::-1]:
            for role in self.roles[::-1]:
                if item.RoleId == role.ParentRole and "Kolizija" in role.Name:
                    return item, role
        
        return None

    


def setup(client):
    client.add_cog(Rankup(client))