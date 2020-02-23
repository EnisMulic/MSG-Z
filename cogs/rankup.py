import discord
from discord.ext import commands
from discord.ext import tasks

from models.role import Role

class Rankup(commands.Cog):
    def __init__(self, client):
        self.client = client

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
        pass

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def apsolvent(self, ctx):
        pass

    @commands.command(aliases=["diplomirao", "diplomirala"])
    @commands.has_any_role('Administrator') 
    async def diploma(self, ctx):
        pass

    @commands.command(aliases=["alumni", "alumna"])
    @commands.has_any_role('Administrator') 
    async def alum(self, ctx):
        pass

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def uslov(self, ctx):
        pass

    @commands.command(aliases=["obnovio", "obnovila"])
    @commands.has_any_role('Administrator') 
    async def obnova(self, ctx):
        pass

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def ispis(self, ctx):
        pass

def setup(client):
    client.add_cog(Rankup(client))