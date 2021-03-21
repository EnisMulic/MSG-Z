import discord
from discord.ext import commands
from discord.ext import tasks

import json
import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound


from models.base import Base, Session, engine
from models.user import User
from models.channel import Channel
from models.youtube import Youtube
import models.base as base

import datetime

from utils import misc


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

        Base.metadata.create_all(engine)
        self.session = Session()
        

    def Session(self):
        return base.Session()

                
    @commands.command(aliases=["insert-channel"], description = "Add channel to the database")
    @commands.has_any_role('Administrator') 
    async def insert_channel(self, ctx, channel: discord.TextChannel):
        """Insert channel into database."""

        try:
            newChannel = Channel(channel.id, channel.name)
            self.session.add(newChannel)
            self.session.commit()
        except SQLAlchemyError as err:
            await ctx.send(str(err))
            self.session.rollback()
            

    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def whois(self, ctx, user: discord.User):
        """Get info of user by mention."""

        try:
            member = misc.getMember(self.client, user.id)
            embed = discord.Embed(
                description = member.mention
            )

            embed.set_author(name = member.display_name, icon_url = member.avatar_url)
            embed.set_thumbnail(url = member.avatar_url)
            embed.add_field(
                name = "Registered",
                value = user.created_at.strftime("%a, %b %d, %Y,\n %H:%M %p")
            )

            embed.add_field(
                name = "Joined",
                value = member.joined_at.strftime("%a, %b %d, %Y,\n %H:%M %p")
            )

            roles = [role.mention for role in member.roles[::-1] if role.name != '@everyone']
            embed.add_field(
                name = "Roles",
                value = ' '.join(roles),
                inline = False
            )
            
            await ctx.send(embed = embed)

            
        except NoResultFound as err:
            await ctx.send(str(err))
        
            

    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def student(self, ctx, user_index):
        """Get info of user by student index."""

        try:
            user = self.session.query(User) \
                    .filter(User.UserIndex == user_index) \
                    .one()
            
            member = misc.getMember(self.client, user.UserId)
            
            embed = discord.Embed(
                description = member.mention
            )

            embed.set_author(name = member.display_name, icon_url = member.avatar_url)
            embed.set_thumbnail(url = member.avatar_url)
            embed.add_field(
                name = "Index",
                value = user.UserIndex
            )

            embed.add_field(
                name = "Discord status",
                value = user.StatusDiscord
            )

            roles = [role.mention for role in member.roles[::-1] if role.name != '@everyone']
            embed.add_field(
                name = "Roles",
                value = ' '.join(roles),
                inline = False
            )
            
            await ctx.send(embed = embed)

        except NoResultFound as err:
            await ctx.send(str(err))

        self.session.rollback()


def setup(client):
    client.add_cog(Database(client))

