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
from models.channel import Channel
from models.youtube import Youtube
from models.users_channels import UsersChannelsActivity

import datetime

from utils import misc


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.message_point_multiplier = 0.25

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def report_text(self, ctx, channel: discord.TextChannel):
        f = open(f"./Archive/{channel.name}.txt", "w", encoding="utf-8")
        messages = await channel.history(oldest_first = True, limit = None).flatten()
        for message in messages:
            f.write("Author: " + message.author.name + " | " + str(message.author.id) + " | " 
               + str(message.created_at) + " | " + str(len(message.content))
               + "\n---------------------------------------\n")
        f.close()

    @commands.command(aliases = ["Populate"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def populate(self, ctx):
        session = base.Session()
        # channels_in_db = session.query(Channel)
        # users_in_db = session.query(User)
        for guild in self.client.guilds:
            for channel in guild.channels:
                if session.query(Channel).filter(Channel.Id == channel.id).one_or_none() is not None:
                    messages = await channel.history(oldest_first = True, limit = None).flatten()
                    for message in messages:
                        if session.query(User).filter(User.UserId == message.author.id).one_or_none() is not None:
                            usersAcctivity = session.query(UsersChannelsActivity) \
                                .filter(UsersChannelsActivity.UserId == message.author.id and \
                                        UsersChannelsActivity.ChannelId == channel.id).one_or_none()
                            if usersAcctivity is not None:
                                usersAcctivity.NumberOfMessages = usersAcctivity.NumberOfMessages + 1
                                usersAcctivity.LengthOfMessages = usersAcctivity.LengthOfMessages + len(message.content)
                                usersAcctivity.Points = usersAcctivity.Points + int(len(message.content) * self.message_point_multiplier)
                                
                                session.commit()
                            else:
                                usersAcctivity = UsersChannelsActivity(
                                    UserId = int(message.author.id), 
                                    ChannelId = int(channel.id), 
                                    NumberOfMessages = 1, 
                                    LengthOfMessages = int(len(message.content)),
                                    Points = int(len(message.content) * self.message_point_multiplier)
                                )

                                session.add(usersAcctivity)
                                session.commit()
                        else:
                            try:
                                f = open(f"./Archive/{message.author.name}.txt", "a", encoding="utf-8")
                                f.write(channel.name + " | " + str(len(message.content)) + " = " + 
                                    str(len(message.content) * self.message_point_multiplier)
                                    + "\n---------------------------------------\n")
                                f.close()
                            except:
                                print("Name is wrong")

                # try:
                #     dbChannel = session.query(Channel).filter(channel.id == Channel.Id).one()
                #     print("Found channel " + channel.name)
                #     messages = await channel.history(oldest_first = True, limit = None).flatten()
                #     for message in messages:
                        
                #         try:
                #             dbUser = session.query(User).filter(message.author.id == User.UserId).one()
                #             print("DbUserID: " + dbUser.UserId)
                #             print("------------------------------------")
                #             try:
                            
                #                 print("Found user " + dbUser.Name)
                #                 dbUserActivity = None
                #                 dbUserActivity = session.query(UsersChannelsActivity) \
                #                     .filter(dbUser.UserId == User.UserId and channel.id == Channel.Id).one()
                                
                                
                #                 print("User has activity")
                #                 print(str(dbUserActivity.UserId))
                #                 dbUserActivity.NumberOfMessages = dbUserActivity.NumberOfMessages + 1
                #                 dbUserActivity.LengthOfMessages = dbUserActivity.LengthOfMessages + len(message.content)
                #                 dbUserActivity.Points = dbUserActivity.Points + int(len(message.content) * self.message_point_multiplier)
                            
                #                 session.commit()
                #                 # else:
                #                 #     print("User had no activity")
                #                 #     dbUserActivity = UsersChannelsActivity(
                #                 #         message.author.id, 
                #                 #         channel.id, 
                #                 #         1, 
                #                 #         len(message.content),
                #                 #         len(message.content) * self.message_point_multiplier
                #                 #     )
                #                 #     print(dbUserActivity.UserId)
                #                 #     session.add(dbUserActivity)
                #                 #     session.commit()
                #             except Exception as err:
                #                 print(str(err))
                #                 newUserChannelActivity = UsersChannelsActivity(
                #                     UserId = int(message.author.id), 
                #                     ChannelId = int(channel.id), 
                #                     NumberOfMessages = 1, 
                #                     LengthOfMessages = int(len(message.content)),
                #                     Points = int(len(message.content) * self.message_point_multiplier)
                #                 )

                #                 session.add(newUserChannelActivity)
                #                 session.commit()
                #         except:
                #             f = open(f"./Archive/{message.author.name}.txt", "a", encoding="utf-8")
                #             f.write(channel.name + " | " + str(len(message.content)) + " = " + 
                #                 str(len(message.content) * self.message_point_multiplier)
                #                 + "\n---------------------------------------\n")
                #             f.close()
                        
                # except Exception as err:
                #     print(str(err))


    @commands.command(aliases = ["Top10"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def get_top_10(self, ctx):
        database = self.client.get_cog("Database")
        if database is not None:
            print("Here")
            try:
                session = database.Session()

                users = session.query(User) \
                    .order_by(User.Points.desc()) \
                    .limit(10) \
                    .all()

                for user in users:
                    await ctx.send(user.Name + " " + str(user.Points))
            except SQLAlchemyError as err:
                print(str(err))
            finally:
                session.close()



def setup(client):
    client.add_cog(Leaderboard(client))