import discord
from discord.ext import commands
from discord.ext import tasks

from models.role import Role
from models.user import users_roles_association
from models.user import User

from utils import misc

class Rankup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.roleName = "Registrovan";
        self.role = self.SetRole(self.roleName)

    def SetRole(self, roleName):
        return misc.getRoleByName(self.client, roleName)

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
                session.commit()

            session.close()

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def imatrikulant(self, ctx):
        await ctx.author.add_roles(self.role)
        # embed

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def apsolvent(self, ctx):
        await ctx.author.add_roles(self.role)
        # embed

    @commands.command(aliases=["diplomirao", "diplomirala"])
    @commands.has_any_role('Administrator') 
    async def diploma(self, ctx):
        await ctx.autor.kick(reason = "Diplomirao/Diplomirala")
        # update fakultet status
        # embed

    @commands.command(aliases=["alumni", "alumna"])
    @commands.has_any_role('Administrator') 
    async def alum(self, ctx):
        alumRole = misc.getRoleByName(self.client, "Alumni")
        pass

    @commands.command(aliases=["ocistio", "ocistila"])
    @commands.has_any_role('Administrator') 
    async def cista(self, ctx):
        # see current role
        # get higher role
        # add higher role
        # remove lower role
        pass


    @commands.command()
    @commands.has_any_role('Administrator') 
    async def uslov(self, ctx):
        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()

            roles = ctx.author.roles
            rankedRoles = session.query(Role) \
                .join(users_roles_association) \
                .filter(Role.ParentRole != None) \
                .filter(users_roles_association.c.UserId == ctx.author.id) \
                .all()
                
            # for role in roles not in rankedRoles:
            #     roles.remove(role)
            # for role in rankedRoles:
            #     print(role.Name)

            # rankedRolesIDs = [role.RoleId for role in rankedRoles]
            # usersRankedRoles = [role for role in roles if role.id in rankedRolesIDs]

            # for role in usersRankedRoles:
            #     print(role.name)

            for role in rankedRoles:
                print(role.Name)
        # see current role
        # get higher role
        # add the higher role
        pass

    @commands.command(aliases=["obnovio", "obnovila"])
    @commands.has_any_role('Administrator') 
    async def obnova(self, ctx):
        await ctx.author.add_roles(self.role)
        # embed

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def ispis(self, ctx):
        await ctx.autor.kick(reason = "Ispis")
        # update fakultet status
        # embed

    def findHighestRole(self, roles: []):
        pass

def setup(client):
    client.add_cog(Rankup(client))