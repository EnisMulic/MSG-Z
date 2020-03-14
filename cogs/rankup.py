import discord
from discord.ext import commands
from discord.ext import tasks

import datetime

from models.role import Role
from models.user import users_roles_association
from models.user import User

from utils import misc

def is_in_channel(ctx):
    return ctx.channel.name == 'promocije' or ctx.channel.name == 'logger'

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
        self.roleName = "Registrovan";
        self.role = None
        self.roles = None

    def SetRole(self):
        if self.role is None:
            self.role = misc.getRoleByName(self.client, self.roleName)

    def SetValue(self, role: Role):
        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()

            if role.ParentRole is not None:
                parent = session.query(Role) \
                    .filter(Role.RoleId == role.ParentRole) \
                    .one()
                
                children = session.query(Role) \
                    .filter(Role.ParentRole == role.ParentRole) \
                    .count()

                role.Value = parent.Value + 1 + children * 0.1
            else:
                role.Value = 0
    
    def formRoles(self):
        if self.roles is None:
            database = self.client.get_cog("Database")
            if database is not None:
                session = database.Session()
                rankedRoles = session.query(Role) \
                        .filter(Role.ParentRole != None) \
                        .all()

                RoleTree = SortTree(rankedRoles[0])
                for rankedRole in rankedRoles[1:]:
                    RoleTree.insert_val(rankedRole)

                
                self.roles = display(RoleTree)

    def getUsersRankedRoles(self, user):
        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()

            rankedRoles = session.query(Role) \
                    .join(users_roles_association) \
                    .filter(Role.ParentRole != None) \
                    .filter(users_roles_association.c.UserId == user.id) \
                    .all()

            session.close()

            return rankedRoles

    
    @commands.command()
    @commands.has_any_role('Administrator') 
    async def connect(self, ctx, parentRole: discord.Role, childRole: discord.Role):
        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()
            parent = session.query(Role) \
                .filter(Role.RoleId == parentRole.id) \
                .one_or_none()

            child = session.query(Role) \
                .filter(Role.RoleId == childRole.id) \
                .one_or_none()

            if parent is not None and child is not None:
                child.ParentRole = parent.RoleId
                self.SetValue(child)
                session.commit()

            session.close()

    
    @commands.command()
    @commands.check(is_in_channel) 
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

    
    @commands.command(aliases=["diplomirao", "diplomirala"])
    @commands.check(is_in_channel)
    async def diploma(self, ctx):
        # self.SetRole()
        await ctx.author.kick(reason = "Diplomirao/Diplomirala")
        # update fakultet status
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je diplomirao/diplomirala :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    
    @commands.command(aliases=["alumni", "alumna"])
    @commands.check(is_in_channel) 
    async def alum(self, ctx):
        # self.SetRole()
        alumRole = misc.getRoleByName(self.client, "Alumni")
        await ctx.author.add_roles(alumRole)
        rankedRoles = self.getUsersRankedRoles(ctx.author)

        for role in ctx.author.roles:
            for rankedRole in rankedRoles:
                if role.id == rankedRole.RoleId:
                    await ctx.author.remove_roles(role)

        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je diplomirao/diplomirala :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)
    
    
    @commands.command(aliases=["ocistio", "ocistila"])
    @commands.check(is_in_channel) 
    async def cista(self, ctx):
        self.SetRole()
        rankedRoles = self.getUsersRankedRoles(ctx.author)
        highestRole, nextRole = self.findNextRole(rankedRoles)
        
        for role in ctx.author.roles:
            for rankedRole in rankedRoles:
                if role.id == rankedRole.RoleId:
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
        rankedRoles = self.getUsersRankedRoles(ctx.author)
        
        highestRole, nextRole = self.findNextRole(rankedRoles)
        nextRole = misc.getRoleById(self.client, nextRole.RoleId)


        for role in ctx.author.roles:
            for rankedRole in rankedRoles:
                if role.id == rankedRole.RoleId and role.id != highestRole.RoleId:
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
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " je obnovio/obnovila :tada:"
        )

        embed.set_author(name = ctx.author.display_name, icon_url = ctx.author.avatar_url)
        embed.set_thumbnail(url = ctx.author.avatar_url)

        await ctx.send(embed = embed)

    
    @commands.command()
    @commands.check(is_in_channel) 
    async def kolizija(self, ctx):
        self.SetRole()

        
        rankedRoles = self.getUsersRankedRoles(ctx.author)
        highestRole, nextRole = self.findNextRoleKolizija(rankedRoles)
        
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
        # update fakultet status
        
        embed = discord.Embed(
            colour = discord.Colour.gold().value,
            description = "\n :tada: " + ctx.author.mention + " se ispisao/ispisala :tada:"
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