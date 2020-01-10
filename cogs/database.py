import discord
from discord.ext import commands
from discord.ext import tasks

import json
import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import models.base as base
from models.base import Base, Session, engine
from models.post import Post
from models.role import Role
from models.user import User
from models.youtube import Youtube



from utils import misc


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.detect_anomalies.start()

        Base.metadata.create_all(engine)
        self.session = Session()

    def Session(self):
        return base.Session();
            

    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def whois(self, ctx, member: discord.Member):
        try:
            user = self.session.query(User) \
                    .filter(User.UserId == member.id) \
                    .one()

            await ctx.send('```\nIme i prezime: {}\nIndex: {}\nUsername: {}\nFakultet: {}\nDiscord: {}\n```'
                    .format(
                            user.Name,
                            user.UserIndex,
                            user.Username + "#" + user.Discriminator,
                            user.StatusFakultet,
                            user.StatusDiscord
                        ))
        except SQLAlchemyError as err:
            print(str(err))
            

    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def student(self, ctx, userIndex: str):
        try:
            user = self.session.query(User) \
                    .filter(User.UserIndex == userIndex) \
                    .one()
                    
            await ctx.send('```\nIme i prezime: {}\nIndex: {}\nUsername: {}\nFakultet: {}\nDiscord: {}\n```'
                    .format(
                            user.Name,
                            user.UserIndex,
                            user.Username + "#" + user.Discriminator,
                            user.StatusFakultet,
                            user.StatusDiscord
                        ))
        except SQLAlchemyError as err:
            print(str(err))


    @tasks.loop(hours = 7 * 24)
    async def detect_anomalies(self):
        print("Anomalysing...")

        
        allRoles = self.session.query(Role).all()
        
        for guild in self.client.guilds:                                                        
            for member in guild.members:
                try:
                    user = self.session.query(User) \
                            .filter(User.UserId == member.id) \
                            .one()


                    if user is not None:
                        if user.Name != member.nick:
                            user.Name = member.nick
                                
                        if user.Username != member.name:
                            user.Username = member.name
                            
                        if user.Discriminator != member.discriminator:
                            user.Discriminator = member.discriminator


                        memberRoles = []
                        for role in member.roles:
                            memberRoles.append(Role(role.id, role.name))
                        

                        for memberRole in memberRoles:
                            if memberRole in allRoles:
                                if memberRole not in user.Roles:
                                    try:
                                        user.Roles.append(memberRole)
                                    except Exception as err:
                                        print(err)

                        for dbRole in user.Roles:
                            if dbRole not in memberRoles:
                                user.Roles.remove(dbRole)
                                   
                
                except SQLAlchemyError as err:
                    print(member.name + " not in the database")
                

    def cog_unload(self):
        self.detect_anomalies.cancel()

    @detect_anomalies.before_loop
    async def before_detect_anomalies(self):
        print('Database: Waiting...')
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Database(client))

