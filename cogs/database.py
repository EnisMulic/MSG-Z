import discord
from discord.ext import commands

from sqlalchemy.orm.exc import NoResultFound

from models.base import Base, Session, engine
from models.user import User
import models.base as base

from constants import roles
from utils import misc

class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

        Base.metadata.create_all(engine)
        self.session = Session()
        

    def Session(self):
        return base.Session()
            

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def whois(self, ctx, user: discord.User):
        """Get user info by mention."""

        try:
            user = self.session.query(User) \
                    .filter(User.UserId == user.id) \
                    .one()
            
            member = misc.get_member(self.client, user.UserId)

            embed = self._get_embed_for_member(user, member)
            
            await ctx.send(embed = embed)

            
        except NoResultFound as err:
            await ctx.send(str(err))
         

    @commands.command()
    @commands.has_any_role(roles.ADMINISTRATOR, roles.MODERATOR)
    async def student(self, ctx, user_index):
        """Get user info by student index."""

        try:
            user = self.session.query(User) \
                    .filter(User.UserIndex == user_index) \
                    .one()
            
            member = misc.get_member(self.client, user.UserId)

            if member is None:
                embed = self._get_embed_for_user(user)
                await ctx.send(embed = embed)
            else:
                embed = self._get_embed_for_member(user, member)
                await ctx.send(embed = embed)

        except NoResultFound as err:
            await ctx.send(str(err))

    def _get_embed_for_user(self, user: User):
        embed = discord.Embed()

        embed.add_field(name="Mention", value=f'<@!{user.UserId}>', inline=True)
        embed.add_field(name="Name", value=user.Name, inline=True)
        embed.add_field(name="Index", value=user.UserIndex, inline=True)

        return embed

    def _get_embed_for_member(self, user: User, member: discord.User):
        embed = discord.Embed()

        embed.set_author(name = member.display_name, icon_url = member.avatar_url)
        embed.set_thumbnail(url = member.avatar_url)

        embed.add_field(name="Mention", value=f'<@{member.id}>', inline=True)
        embed.add_field(name="Index", value=user.UserIndex, inline=True)

        roles = [role.mention for role in member.roles[::-1] if role.name != '@everyone']
        embed.add_field(
            name = "Roles",
            value = ' '.join(roles),
            inline = False
        )

        return embed


def setup(client):
    client.add_cog(Database(client))

