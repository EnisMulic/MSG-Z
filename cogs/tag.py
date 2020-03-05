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
    async def add_text_tag(self, ctx, name: str, *, content):
        self._add_tag(ctx, "Text", name, content)
        await ctx.send("Tag added")

    @commands.command(aliases=["add-link"])
    async def add_link_tag_tag(self, ctx, name: str, link: str):
        if re.match("^https:[a-zA-Z0-9_.+-/#~]+$", link) is not None:
            self._add_tag(ctx, "Link", name, link)
            await ctx.send("Link added")
    

    def _add_tag(self, ctx, tag_type, name, content):
        name = name.strip('\"')
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                user = session.query(User) \
                        .filter(User.UserId == ctx.author.id) \
                        .one()
        
                newTag = tg.Tag(name, tag_type, content, datetime.datetime.now(), user)
                session.add(newTag)
                session.commit()
            except SQLAlchemyError as err:
                print(str(err))
                session.rollback()
            finally:
                session.close()


    @commands.command(aliases=["remove-tag"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_text_tag(self, ctx, name: str):
        await self._remove_tag(ctx, name)
        await ctx.send("Tag removed")

    @commands.command(aliases=["remove-link"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_link_tag(self, ctx, name: str):
        self._remove_tag(ctx, name)
        await ctx.send("Link removed")

    def _remove_tag(self, ctx, name: str):
        name = name.strip('\"')
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.Id == id) \
                    .one()
                session.delete(tag)
                session.commit()

            except SQLAlchemyError as err:
                print(str(err))
                session.rollback()
            finally:
                session.close()

    @commands.command(aliases=["rename-tag"])
    async def rename_text_tag(self, ctx, old_name: str, new_name: str):
        await self._rename_tag(ctx, old_name, new_name, "tag")

    @commands.command(aliases=["rename-link"])
    async def rename_link_tag(self, ctx, old_name: str, new_name: str):
        await self._rename_tag(self, old_name, new_name, "link")
    
    async def _rename_tag(self, ctx, old_name: str, new_name: str, tag_type: str):
        old_name = old_name.strip('\"')
        new_name = new_name.strip('\"')
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.Name == old_name) \
                    .one()

                if tag.UserId == ctx.author.id:
                    tag.Name = new_name
                    session.commit()

                    await ctx.send(tag_type + " renamed")
                else:
                    await ctx.send("Only the owner can rename the " + tag_type)
            except SQLAlchemyError as err:
                print(str(err))
            finally:
                session.close()

    @commands.command(aliases=["edit-tag"])
    async def edit_text_tag(self, ctx, name: str, *, content: str):
        await self._edit_tag(ctx, name, content, "tag")

    @commands.command(aliases=["edit-link"])
    async def edit_link_tag(self, ctx, name: str, link: str):
        if re.match("^https:[a-zA-Z0-9_.+-/#~]+$", link) is not None:
            await self._edit_tag(ctx, name, link, "link")

    async def _edit_tag(self, ctx, name: str, content: str, tag_type: str):
        name = name.strip('\"')
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                session = database.Session()
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.Name == name) \
                    .one()
                
                if tag.UserId == ctx.author.id:
                    tag.Content = content
                    tag.Count = 0
                    session.commit()
                else:
                    await ctx.send("Only the owner can edit the " + tag_type)
            
            except SQLAlchemyError as err:
                print(str(err))
            finally:
                session.close()
    
    @commands.command(aliases=["tag"])
    async def get_text_tag(self, ctx, *, name: str):
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()
            tag = session.query(tg.Tag) \
                .filter(tg.Tag.Name == name) \
                .one()

            if tag is not None:
                await ctx.send(tag)
                tag.Count += 1
                session.commit()

            session.close()

    @commands.command(aliases=["link"])
    async def get_link_tag(self, ctx, *, search: str):
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
    async def text_tag_info(self, ctx, *, name: str):
        await self._tag_info(ctx, name, "tag")

    @commands.command(aliases=["link-info"])
    async def link_tag_info(self, ctx, *, name: str):
        await self._tag_info(ctx, name, "link")

    async def _tag_info(self, ctx, name: str, tag_type: str):
        name = name.strip('\"')
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()
            try:
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.Name.ilike(f"%{name}%")) \
                    .one()

                member = misc.getMember(self.client, tag.User.UserId)

                embed = discord.Embed(
                    title = ":label:" + tag_type + "info",
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
                    value = f"[{tag.Name}]",
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

    # @commands.command(aliases=["tags"])
    # async def get_link_tags(self, ctx, member: discord.Member = None):
    #     database = self.client.get_cog('Database')
    #     if database is not None:
    #         session = database.Session()

    #         member = member if member is not None else ctx.author
    #         tags = session.query(tg.Tag) \
    #             .filter(tg.Tag.UserId == member.id)


    #         description = "\n"
    #         for tag in tags:
    #             description += f"\n:label: [{tag.Name}]"
    #             tag.Count += 1
                              
    #         embed = discord.Embed(
    #             title = "Users tags",
    #             colour = discord.Colour.blurple()
    #         ) 

    #         embed.add_field(
    #             name = "Owner",
    #             value = "<@" + str(member.id) + ">",
    #             inline = False
    #         )

    #         embed.add_field(
    #             name = "Tags",
    #             value = description,
    #             inline = False
    #         )



            
    #         embed.set_thumbnail(url = member.avatar_url)

            
    #         await ctx.send(embed = embed)
            
    #         session.close()

    @commands.command(aliases=["release-tag"])
    async def release_text_tag(self, ctx, *, name: str):
        await self._release_tag(ctx, name, "tag")


    @commands.command(aliases=["release-link"])
    async def release_link_tag(self, ctx, *, name: str):
        await self._release_tag(ctx, name, "link")

    async def _release_tag(self, ctx, name: str, tag_type: str):
        name = name.strip('\"')
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.UserId == ctx.author.id and tg.Tag.Name == name) \
                    .one()
                
                tag.UserId = None
                session.commit()
                await ctx.send(tag_type + " released")
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()
    
    @commands.command(aliases=["claime-tag"])
    async def claime_text_tag(self, ctx, *, name: str):
        await self._claime_tag(ctx, name, "tag")


    @commands.command(aliases=["claime-link"])
    async def claime_link_tag(self, ctx, *, name: str):
        await self._claime_tag(ctx, name, "link")

    async def _claime_tag(self, ctx, name: str, tag_type: str):
        name = name.strip('\"')
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.UserId == None and tg.Tag.Name == name) \
                    .one()
                
                tag.UserId = ctx.author.id
                session.commit()
                await ctx.send(tag_type + " " + name + " claimed by " + ctx.author.mention)
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()

    @commands.command(aliases=["transfer-tag"])
    async def transfer_text_tag(self, ctx, member: discord.Member, *, name: str):
        await self._transfer_tag(ctx, member, name, "tag")
    

    @commands.command(aliases=["transfer-link"])
    async def transfer_link_tag(self, ctx, member: discord.Member, *, name: str):
        await self._transfer_tag(ctx, member, name, "link")

    async def _transfer_tag(self, ctx, member: discord.Member, name: str, tag_type: str):
        name = name.strip('\"')
        database = self.client.get_cog('Database')
        if database is not None:
            session = database.Session()

            try:
                tag = session.query(tg.Tag) \
                    .filter(tg.Tag.UserId == ctx.author.id and tg.Tag.Name == name) \
                    .one()
                
                tag.UserId = member.id
                session.commit()
                await ctx.send(tag_type + " " + name + " transferred")
            except SQLAlchemyError as err:
                print(err)
                #implement await ctx.send(embed = embed)
            finally:
                session.close()


def setup(client):
    client.add_cog(Tag(client))