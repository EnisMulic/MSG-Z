from os import remove
import discord
from discord.ext import commands

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

import datetime

from models.user import User
import models.base as base

from constants import roles, channels

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = base.Session()

    @commands.command(aliases=["add-member", "am"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def add_member(self, ctx, member: discord.Member, index: str):
        try:
            member_nick = member.nick if member.nick is not None else member.name

            user = User(
                member.id, index, member_nick, 
                member.name, member.discriminator
            )

            self.session.add(user)
            self.session.commit()
                            
            await ctx.reply("Member added")
        except SQLAlchemyError as err:
            await ctx.reply(str(err))
            self.session.rollback()

    @commands.command(aliases=["update-member", "um"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def update_member(self, ctx, new: discord.Member, index: str):
        try:
            user = self.session.query(User) \
                .filter(User.Index == index) \
                .one()
            
            if user is not None:
                old_account = discord.utils.get(self.bot.get_all_members(), id=user.DiscordId)

                member_nick = new.nick if new.nick is not None else new.name

                user.DiscordId = new.id
                user.Username = new.name
                user.Discriminator = new.discriminator
                user.Name = member_nick

                await old_account.kick()
                
                self.session.commit()

                await ctx.reply("Member changed")
        except SQLAlchemyError as err:
            await ctx.reply(str(err))
            self.session.rollback()

    @commands.command(aliases=["set-index", "si"])
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def set_index(self, ctx, member: discord.Member, index: str):
        try:
            user = self.session.query(User) \
                .filter(User.DiscordId == member.id) \
                .one()
            
            if user is not None:
                user.Index = index
                self.session.commit()
            
                await ctx.reply("Index set")
        except SQLAlchemyError as err:
            await ctx.reply(str(err))

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def student(self, ctx, index):
        """Get user info by student index."""

        try:
            user = self.session.query(User) \
                .filter(User.Index == index) \
                .one()
            
            embed = discord.Embed()
            embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)

            embed.add_field(name="Mention", value=f'<@!{user.DiscordId}>', inline=True)
            embed.add_field(name="Name", value=user.Name, inline=True)
            embed.add_field(name="Index", value=user.Index, inline=True)

            await ctx.reply(embed = embed)

        except NoResultFound as err:
            await ctx.reply(str(err))


    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def whois(self, ctx, member: discord.Member):
        """Get user info by mention."""

        try:
            user = self.session.query(User) \
                .filter(User.DiscordId == member.id) \
                .one()
            
            embed = discord.Embed()
            embed.set_author(name="FIT | Community", url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)

            embed.add_field(name="Mention", value=member.mention, inline=True)
            embed.add_field(name="Name", value=user.Name, inline=True)
            embed.add_field(name="Index", value=user.Index, inline=True)
            embed.add_field(name="Created", value=member.created_at.replace(microsecond=0).isoformat(' '), inline=True)
            embed.add_field(name="Joined", value=member.joined_at.replace(microsecond=0).isoformat(' '), inline=True)

            await ctx.reply(embed = embed)

        except NoResultFound as err:
            await ctx.reply(str(err))

    @commands.command(aliases=["to-imatrikulant", "toi"])
    @commands.has_any_role(roles.ADMINISTRATOR)
    async def to_imatrikulant(self, ctx):
        imatrikulant_role = discord.utils.get(ctx.guild.roles, name=roles.IMATRIKULANT)
        apsolvet_role = discord.utils.get(ctx.guild.roles, name=roles.APSOLVENT)

        for member in ctx.guild.members:
            if apsolvet_role in member.roles:
                await member.add_roles(imatrikulant_role)
                await member.remove_roles(apsolvet_role)

def setup(bot):
    bot.add_cog(Member(bot))