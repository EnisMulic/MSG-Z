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




class Tag(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["add-tag"])
    async def add_tag(self, ctx, link: str, *name: str):
        if re.match("^https:[a-zA-Z0-9_.+-/#~]+$", link) is not None:
            tag_name = ' '.join(name)
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
    async def rename_tag(self, ctx, id: int, *name: str):
        tag_name = ' '.join(name)
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
                description += f"\n:bookmark: | [{tag.Name}]({tag.Link})"
                tag.Count += 1
                              
            embed = discord.Embed(
                title = "Tags",
                description = description,
                colour = discord.Colour.blurple().value
            ) 
            
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

                embed = discord.Embed(
                    title = ":bookmark: Tag info",
                    colour = discord.Colour.blurple().value
                ) 

                embed.add_field(
                    name = "Id",
                    value = str(tag.Id),
                    inline = True
                )

                embed.add_field(
                    name = "Name",
                    value = f"[{tag.Name}]({tag.Link})",
                    inline = True
                )

                embed.add_field(
                    name = "Count",
                    value = str(tag.Count),
                    inline = False
                )

                embed.add_field(
                    name = "Created at",
                    value = tag.Created.strftime("%d.%m.%Y %H:%M:%S"),
                    inline = True
                )

                embed.add_field(
                    name = "Owner",
                    value = "<@" + str(tag.User.UserId) + ">",
                    inline = False
                )

                
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

            memberId = member.id if member is not None else ctx.author.id
            tags = session.query(tg.Tag) \
                .filter(tg.Tag.UserId == memberId)


            description = "<@" + str(memberId) + ">\n"
            for tag in tags:
                description += f"\n:bookmark: | [{tag.Name}]({tag.Link})"
                tag.Count += 1
                              
            embed = discord.Embed(
                title = "Tags",
                description = description,
                colour = discord.Colour.blurple().value
            ) 

            embed.set_author
            
            await ctx.send(embed = embed)
            
            session.close()

def setup(client):
    client.add_cog(Tag(client))
