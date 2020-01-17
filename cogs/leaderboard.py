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

import datetime

from utils import misc


class Leaderboard(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role('Administrator') 
    async def report_text(self, ctx, channel: discord.TextChannel):
        f = open(f"./Archive/{channel.name}.txt", "w", encoding="utf-8")
        messages = await channel.history(oldest_first = True, limit = None).flatten()
        for message in messages:
            f.write("Author: " + message.author.name + " | " + str(message.author.id) + " | " 
               + str(message.created_at)
               + "\n---------------------------------------\n")
        f.close()


def setup(client):
    client.add_cog(Leaderboard(client))