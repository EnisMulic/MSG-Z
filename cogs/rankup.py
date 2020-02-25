import discord
from discord.ext import commands
from discord.ext import tasks

from models.role import Role

from utils import misc

class Rankup(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.roleName = "Registrovan";
        self.role = self.SetRole(self.roleName)

    def SetRole(self, roleName):
        return self.client.get_role(misc.getRoleId(self.client, roleName))

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def connect(self, ctx, lowRole: discord.Role, highRole: discord.Role):
        database = self.client.get_cog("Database")
        if database is not None:
            session = database.Session()
            role = session.query(Role) \
                .filter(Role.RoleId == lowRole.id) \
                .one_or_none()

            higherRole = session.query(Role) \
                .filter(Role.RoleId == highRole.id) \
                .one_or_none()

            if role is not None and higherRole is not None:
                role.HigherRole = higherRole.RoleId
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
        alumRole = self.client.get_role(misc.getRoleId(self.client, "Alumni"))
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
                .filter(Role.HigherRole != None) \
                .all()

            for role in roles not in rankedRoles:
                roles.remove(role)
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