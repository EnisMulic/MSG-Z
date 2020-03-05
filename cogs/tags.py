import discord
from discord.ext import commands, tasks


import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import models.link as lnk
from models.user import User

import string
import random
import datetime
import re

from utils import misc

class Link(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["add-link"])
    async def add_link(self, ctx, link: str, *, name: str):
        if re.match("^https:[a-zA-Z0-9_.+-/#~]+$", link) is not None:
            database = self.client.get_cog('Database')
            if database is not None:
                try:
                    session = database.Session()

                    user = session.query(User) \
                            .filter(User.UserId == ctx.author.id) \
                            .one()


                    newLink = lnk.Link(tag_name, link, datetime.datetime.now(), user)
                    session.add(newTag)
                    session.commit()

                    await ctx.send("Tag added")
                except SQLAlchemyError as err:
                    print(str(err))
                    session.rollback()
                finally:
                    session.close()

    @commands.command(aliases=["remove-link"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_link(self, ctx, id: int):
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                tag = session.query(lnk.Link) \
                    .filter(lnk.Link.Id == id) \
                    .one()
                session.delete(tag)
                session.commit()

                await ctx.send("Tag removed")
            except SQLAlchemyError as err:
                print(str(err))
                session.rollback()
            finally:
                session.close()


    @commands.command(aliases=["rename-link"])
    #@commands.has_any_role('Administrator', 'Moderator')
    async def rename_link(self, ctx, id: int, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                link = session.query(lnk.Link) \
                    .filter(lnk.Link.Id == id) \
                    .one()

                if link.UserId == ctx.author.id:
                    link.Name = name
                    session.commit()

                    await ctx.send("Tag renamed")
                else:
                    await ctx.send("Only the owner can rename the tag")
            except SQLAlchemyError as err:
                print(str(err))
            finally:
                session.close()
    
    @commands.command(aliases=["edit-link"])
    #@commands.has_any_role('Administrator', 'Moderator')
    async def edit_link(self, ctx, id: int, link: str):
        if re.match("^https:[a-zA-Z0-9_.+-/#~]+$", link) is not None:
            database = self.client.get_cog('Database')
            if database is not None:
                try:
                    session = database.Session()
                    link = session.query(lnk.Link) \
                        .filter(lnk.Link.Id == id) \
                        .one()
                    

                    if link.UserId == ctx.author.id:
                        link.Link = link
                        link.Count = 0
                        session.commit()
                    else:
                        await ctx.send("Only the owner can edit the tag")
                

                except SQLAlchemyError as err:
                    print(str(err))
                finally:
                    session.close()

    @commands.command(aliases=["link"])
    async def get_link(self, ctx, *, search: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()
            links = session.query(lnk.Link) \
                .filter(lnk.Link.Name.ilike(f"%{search}%"))


            description = '\n'
            for link in links:
                description += f"\n:label: [{link.Name}]({link.Link})"
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

    @commands.command(aliases=["link-info"])
    async def link_info(self, ctx, *, search: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()
            try:
                link = session.query(lnk.Link) \
                    .filter(lnk.Link.Name.ilike(f"%{search}%")) \
                    .one()

                member = misc.getMember(self.client, link.User.UserId)

                embed = discord.Embed(
                    title = ":label: Tag info",
                    colour = discord.Colour.blurple()
                ) 

                embed.add_field(
                    name = "Id",
                    value = str(link.Id),
                    inline = True
                )

                embed.add_field(
                    name = "Count",
                    value = str(link.Count),
                    inline = True
                )

                embed.add_field(
                    name = "Name",
                    value = f"[{link.Name}]({link.Link})",
                    inline = True
                )

                embed.add_field(
                    name = "Owner",
                    value = member.mention,
                    inline = False
                )

                embed.add_field(
                    name = "Link created at",
                    value = link.Created.strftime("%d.%m.%Y %H:%M:%S"),
                    inline = True
                )

                

                
                embed.set_thumbnail(url = member.avatar_url)

                
                await ctx.send(embed = embed)
            except SQLAlchemyError as err:
                print(str(err))
            finally:
                session.close()

    @commands.command(aliases=["links"])
    async def get_links(self, ctx, member: discord.Member = None):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            member = member if member is not None else ctx.author
            links = session.query(lnk.Link) \
                .filter(lnk.Link.UserId == member.id)


            description = "\n"
            for link in links:
                description += f"\n:label: [{link.Name}]({link.Link})"
                link.Count += 1
                              
            embed = discord.Embed(
                title = "Users links",
                colour = discord.Colour.blurple()
            ) 

            embed.add_field(
                name = "Owner",
                value = "<@" + str(member.id) + ">",
                inline = False
            )

            embed.add_field(
                name = "Links",
                value = description,
                inline = False
            )



            
            embed.set_thumbnail(url = member.avatar_url)

            
            await ctx.send(embed = embed)
            
            session.close()

    @commands.command(aliases=["release-link"])
    async def release_link(self, ctx, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                link = session.query(lnk.Link) \
                    .filter(lnk.Link.UserId == ctx.author.id and lnk.Link.Name == name) \
                    .one()
                
                link.UserId = None
                session.commit()
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()
    
    @commands.command(aliases=["claime-link"])
    async def claime_link(self, ctx, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                link = session.query(lnk.Link) \
                    .filter(lnk.Link.UserId == None and lnk.Link.Name == name) \
                    .one()
                
                link.UserId = ctx.author.id
                session.commit()
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()

    @commands.command(aliases=["transfer-link"])
    async def transfer_link(self, ctx, member: discord.Member, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                link = session.query(lnk.Link) \
                    .filter(lnk.Link.UserId == ctx.author.id and lnk.Link.Name == name) \
                    .one()
                
                link.UserId = member.id
                session.commit()
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()


def setup(client):
    client.add_cog(Link(client))
