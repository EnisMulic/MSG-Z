import discord
from discord.ext import commands, tasks

import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import models.tag as tg
from models.user import User
import models.base as base

import string
import random
import datetime
import re

from utils import misc

from enum import Enum

class TagType(Enum):
    LINK = "Link"
    TEXT = "Text"

class Tag(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.linkRegex = "^https:[a-zA-Z0-9_.+-/:?=#~]+$"
        self.session = base.Session()

    @commands.command(aliases=["add-tag"])
    async def add_text_tag(self, ctx, name: str, *, content):
        content = content.strip('\"')
        await self._add_tag(ctx, TagType.TEXT.name, name, content)
        

    @commands.command(aliases=["add-link"])
    async def add_link_tag(self, ctx, name: str, link: str):
        if re.match(self.linkRegex, link) is not None:
            await self._add_tag(ctx, TagType.LINK.name, name, link)
    

    async def _add_tag(self, ctx, tag_type, name, content):
        name = name.strip('\"')
        
        try:
            user = self.session.query(User) \
                    .filter(User.UserId == ctx.author.id) \
                    .one()
    
            new_tag = tg.Tag(name, tag_type, content, datetime.datetime.now(), user)

            self.session.add(new_tag)
            self.session.commit()

            await ctx.send(tag_type + " added")
        except SQLAlchemyError as err:
            print(str(err))
            self.session.rollback()


    @commands.command(aliases=["remove-tag"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_text_tag(self, ctx, name: str):
        await self._remove_tag(ctx, name, TagType.TEXT.name)

    @commands.command(aliases=["remove-link"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_link_tag(self, ctx, name: str):
        await self._remove_tag(ctx, name, TagType.LINK.name)

    async def _remove_tag(self, ctx, name: str, tag_type: str):
        name = name.strip('\"')
        
        try:
            tag = self.session.query(tg.Tag) \
                .filter(tg.Tag.Name == name) \
                .filter(tg.Tag.Type == tag_type) \
                .one()
            
            self.session.delete(tag)
            self.session.commit()
            await ctx.send(tag_type + " removed")
        except SQLAlchemyError as err:
            print(str(err))
            self.session.rollback()

    @commands.command(aliases=["rename-tag"])
    async def rename_text_tag(self, ctx, old_name: str, new_name: str):
        await self._rename_tag(ctx, old_name, new_name, TagType.TEXT.name)

    @commands.command(aliases=["rename-link"])
    async def rename_link_tag(self, ctx, old_name: str, new_name: str):
        await self._rename_tag(ctx, old_name, new_name, TagType.LINK.name)
    
    async def _rename_tag(self, ctx, old_name: str, new_name: str, tag_type: str):
        old_name = old_name.strip('\"')
        new_name = new_name.strip('\"')
        
        try:
            tag = self.session.query(tg.Tag) \
                .filter(tg.Tag.Name == old_name) \
                .filter(tg.Tag.Type == tag_type) \
                .one()
        
            if tag.UserId == ctx.author.id:
                tag.Name = new_name
                self.session.commit()
                await ctx.send(tag_type + " renamed")
            else:
                await ctx.send("Only the owner can rename the " + tag_type)
        
        except SQLAlchemyError as err:
            print(str(err))

    @commands.command(aliases=["edit-tag"])
    async def edit_text_tag(self, ctx, name: str, *, content: str):
        content = content.strip('\"')
        await self._edit_tag(ctx, name, content, TagType.TEXT.name)

    @commands.command(aliases=["edit-link"])
    async def edit_link_tag(self, ctx, name: str, link: str):
        if re.match(self.linkRegex, link) is not None:
            await self._edit_tag(ctx, name, link, TagType.LINK.name)

    async def _edit_tag(self, ctx, name: str, content: str, tag_type: str):
        name = name.strip('\"')
        
        try:
            tag = self.session.query(tg.Tag) \
                .filter(tg.Tag.Name == name) \
                .filter(tg.Tag.Type == tag_type) \
                .one()
            
            if tag.UserId == ctx.author.id:
                tag.Content = content
                tag.Count = 0
                self.session.commit()
            else:
                await ctx.send("Only the owner can edit the " + tag_type)
        
        except SQLAlchemyError as err:
            print(str(err))
    
    @commands.command(aliases=["tag"])
    async def get_text_tag(self, ctx, name: str):
        name = name.strip('\"')
        try:
            tag = self.session.query(tg.Tag) \
                .filter(tg.Tag.Name == name and tg.Tag.Type == TagType.TEXT.name) \
                .one()

            if tag is not None:
                await ctx.send(tag.Content)
                tag.Count += 1
                self.session.commit()
        except SQLAlchemyError as err:
            print(str(err))

    @commands.command(aliases=["link"])
    async def get_link_tag(self, ctx, name: str):
        name = name.strip('\"')
        
        try:
            tags = self.session.query(tg.Tag) \
                .filter(tg.Tag.Name.ilike(f"%{name}%")) \
                .filter(tg.Tag.Type == TagType.LINK.name)


            description = '\n'
            for tag in tags:
                description += f"\n[`{tag.Name}`]({tag.Content})"
                tag.Count += 1
                              
            embed = discord.Embed(
                description = "\n" + description,
                colour = discord.Colour.blurple()
            ) 

            await ctx.send(embed = embed)

            self.session.commit()
            self.session.close()
        except SQLAlchemyError as err:
            print(str(err))
        

    @commands.command(aliases=["tag-info"])
    async def info_text_tag(self, ctx, *, name: str):
        await self._info_tag(ctx, name, TagType.TEXT.name)

    @commands.command(aliases=["link-info"])
    async def info_link_tag(self, ctx, *, name: str):
        await self._info_tag(ctx, name, TagType.LINK.name)

    async def _info_tag(self, ctx, name: str, tag_type: str):
        name = name.strip('\"')
        try:
            tag = self.session.query(tg.Tag) \
                .filter(tg.Tag.Name == name) \
                .filter(tg.Tag.Type == tag_type) \
                .one()

            owner = f"<@{tag.User.UserId}>" if tag.User is not None else '@everyone'
            
            embed = discord.Embed(
                title = ":label: " + tag_type + " info",
                colour = discord.Colour.blurple()
            ) 
            
            embed.add_field(
                name = "Owner",
                value = owner,
                inline = True
            )
            embed.add_field(
                name = "Name",
                value = f"{tag.Name}",
                inline = True
            )
            embed.add_field(
                name = "Count",
                value = str(tag.Count),
                inline = True
            )

            embed.add_field(
                name = "Tag created at",
                value = tag.Created.strftime("%d.%m.%Y %H:%M:%S"),
                inline = True
            )
            # embed.set_thumbnail(url = self.client.avatar_url)
            
            await ctx.send(embed = embed)
        except SQLAlchemyError as err:
            print(str(err))


    @commands.command(aliases=["release-tag"])
    async def release_text_tag(self, ctx, *, name: str):
        await self._release_tag(ctx, name, TagType.TEXT.name)


    @commands.command(aliases=["release-link"])
    async def release_link_tag(self, ctx, *, name: str):
        await self._release_tag(ctx, name, TagType.LINK.name)

    async def _release_tag(self, ctx, name: str, tag_type: str):
        name = name.strip('\"')
        
        try:
            tag = self.session.query(tg.Tag) \
                .filter(tg.Tag.UserId == ctx.author.id) \
                .filter(tg.Tag.Name == name) \
                .filter(tg.Tag.Type == tag_type) \
                .one() 
            
            tag.UserId = None
            self.session.commit()
            await ctx.send(tag_type + " released")
        except SQLAlchemyError as err:
            print(err)
            #implement await ctx.send(embed = embed)
    
    @commands.command(aliases=["claim-tag"])
    async def claim_text_tag(self, ctx, *, name: str):
        await self._claim_tag(ctx, name, TagType.TEXT.name)


    @commands.command(aliases=["claim-link"])
    async def claim_link_tag(self, ctx, *, name: str):
        await self._claim_tag(ctx, name, TagType.LINK.name)

    async def _claim_tag(self, ctx, name: str, tag_type: str):
        name = name.strip('\"')
        try:
            tag = self.session.query(tg.Tag) \
                .filter(tg.Tag.UserId == None) \
                .filter(tg.Tag.Name == name) \
                .filter(tg.Tag.Type == tag_type) \
                .one()
            
            tag.UserId = ctx.author.id
            self.session.commit()

            await ctx.send(tag_type + " " + name + " claimed by " + ctx.author.mention)
        except SQLAlchemyError as err:
            print(err)
            #implement await ctx.send(embed = embed)

    @commands.command(aliases=["transfer-tag"])
    async def transfer_text_tag(self, ctx, member: discord.Member, name: str):
        await self._transfer_tag(ctx, member, name, TagType.TEXT.name)
    

    @commands.command(aliases=["transfer-link"])
    async def transfer_link_tag(self, ctx, member: discord.Member, name: str):
        await self._transfer_tag(ctx, member, name, TagType.LINK.name)

    async def _transfer_tag(self, ctx, member: discord.Member, name: str, tag_type: str):
        name = name.strip('\"')
        try:
            tag = self.session.query(tg.Tag) \
                .filter(tg.Tag.UserId == ctx.author.id) \
                .filter(tg.Tag.Name == name) \
                .filter(tg.Tag.Type == tag_type) \
                .one()
            
            tag.UserId = member.id
            self.session.commit()
            await ctx.send(tag_type + " " + name + " transferred")
        except SQLAlchemyError as err:
            print(err)
            #implement await ctx.send(embed = embed)


def setup(client):
    client.add_cog(Tag(client))