import discord
from discord.ext import commands, tasks


import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import models.tag as tg
from models.user import User

import string
import random
import datetime
import re

from utils import misc

class Tag(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["add-tag"])
    async def add_tag(self, ctx, link: str, *, name: str):
        if re.match("^https:[a-zA-Z0-9_.+-/#~]+$", link) is not None:
            database = self.client.get_cog('Database')
            if database is not None:
                try:
                    session = database.Session()

                    user = session.query(User) \
                            .filter(User.UserId == ctx.author.id) \
                            .one()


                    newTag = tg.Tag(tag_name, link, datetime.datetime.now(), user)
                    session.add(newTag)
                    session.commit()

                    await ctx.send("Tag added")
                except SQLAlchemyError as err:
                    print(str(err))
                    session.rollback()
                finally:
                    session.close()

    @commands.command(aliases=["remove-tag"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_tag(self, ctx, id: int):
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.Id == id) \
                    .one()
                session.delete(tag)
                session.commit()

                await ctx.send("Tag removed")
            except SQLAlchemyError as err:
                print(str(err))
                session.rollback()
            finally:
                session.close()


    @commands.command(aliases=["rename-tag"])
    #@commands.has_any_role('Administrator', 'Moderator')
    async def rename_tag(self, ctx, id: int, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.Id == id) \
                    .one()

                if tag.UserId == ctx.author.id:
                    tag.Name = tag_name
                    session.commit()

                    await ctx.send("Tag renamed")
                else:
                    await ctx.send("Only the owner can rename the tag")
            except SQLAlchemyError as err:
                print(str(err))
            finally:
                session.close()
    
    @commands.command(aliases=["edit-tag"])
    #@commands.has_any_role('Administrator', 'Moderator')
    async def edit_tag(self, ctx, id: int, link: str):
        if re.match("^https:[a-zA-Z0-9_.+-/#~]+$", link) is not None:
            database = self.client.get_cog('Database')
            if database is not None:
                try:
                    session = database.Session()
                    tag = session.query(tg.Tag) \
                        .filter(tg.Tag.Id == id) \
                        .one()
                    

                    if tag.UserId == ctx.author.id:
                        tag.Link = link
                        tag.Count = 0
                        session.commit()
                    else:
                        await ctx.send("Only the owner can edit the tag")
                

                except SQLAlchemyError as err:
                    print(str(err))
                finally:
                    session.close()

    @commands.command(aliases=["tag"])
    async def get_tag(self, ctx, *, search: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()
            tags = session.query(tg.Tag) \
                .filter(tg.Tag.Name.ilike(f"%{search}%"))


            description = '\n'
            for tag in tags:
                description += f"\n:label: [{tag.Name}]({tag.Link})"
                tag.Count += 1
                              
            embed = discord.Embed(
                title = "Tags",
                description = description,
                colour = discord.Colour.blurple()
            ) 
            
            embed.set_thumbnail(url = self.client.user.avatar_url)
            
            await ctx.send(embed = embed)
            session.commit()
            session.close()

    @commands.command(aliases=["tag-info"])
    async def tag_info(self, ctx, *, search: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()
            try:
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.Name.ilike(f"%{search}%")) \
                    .one()

                member = misc.getMember(self.client, tag.User.UserId)

                embed = discord.Embed(
                    title = ":label: Tag info",
                    colour = discord.Colour.blurple()
                ) 

                embed.add_field(
                    name = "Id",
                    value = str(tag.Id),
                    inline = True
                )

                embed.add_field(
                    name = "Count",
                    value = str(tag.Count),
                    inline = True
                )

                embed.add_field(
                    name = "Name",
                    value = f"[{tag.Name}]({tag.Link})",
                    inline = True
                )

                embed.add_field(
                    name = "Owner",
                    value = member.mention,
                    inline = False
                )

                embed.add_field(
                    name = "Tag created at",
                    value = tag.Created.strftime("%d.%m.%Y %H:%M:%S"),
                    inline = True
                )

                

                
                embed.set_thumbnail(url = member.avatar_url)

                
                await ctx.send(embed = embed)
            except SQLAlchemyError as err:
                print(str(err))
            finally:
                session.close()

    @commands.command(aliases=["tags"])
    async def get_tags(self, ctx, member: discord.Member = None):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            member = member if member is not None else ctx.author
            tags = session.query(tg.Tag) \
                .filter(tg.Tag.UserId == member.id)


            description = "\n"
            for tag in tags:
                description += f"\n:label: [{tag.Name}]({tag.Link})"
                tag.Count += 1
                              
            embed = discord.Embed(
                title = "Users tags",
                colour = discord.Colour.blurple()
            ) 

            embed.add_field(
                name = "Owner",
                value = "<@" + str(member.id) + ">",
                inline = False
            )

            embed.add_field(
                name = "Tags",
                value = description,
                inline = False
            )



            
            embed.set_thumbnail(url = member.avatar_url)

            
            await ctx.send(embed = embed)
            
            session.close()

    @commands.command(aliases=["release-tags"])
    async def release_tag(self, ctx, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.UserId == ctx.author.id and tg.Tag.Name == name)
                    .one()
                
                tag.UserId = None
                session.commit()
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()
    
    @commands.command(aliases=["claime-tags"])
    async def claime_tag(self, ctx, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.UserId == None and tg.Tag.Name == name)
                    .one()
                
                tag.UserId = ctx.author.id
                session.commit()
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()

    @commands.command(aliases=["transfer-tags"])
    async def transfer_tag(self, ctx, member: discord.Member, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.UserId == ctx.author.id and tg.Tag.Name == name)
                    .one()
                
                tag.UserId = member.id
                session.commit()
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()


def setup(client):
    client.add_cog(Tag(client))
