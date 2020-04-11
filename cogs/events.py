import discord
from discord.ext import commands

import datetime

from utils import logger

from sqlalchemy.exc import SQLAlchemyError

from models.user import User
from models.role import Role
import models.base as base

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.session = base.Session()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            role = discord.utils.get(member.guild.roles, name = "Neregistrovan(a)")
            
            action = discord.Embed(
                title = 'Member Joined',
                colour = discord.Colour.green()
            )
         
            action.add_field(
                name = "Member", 
                value = member.mention + ' ' + member.name + '#' + member.discriminator,
                inline = False
            )
        
            action.add_field(
                name = "Time:", 
                value = str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")),
                inline = False
            )
        
            action.add_field(
                name = "Member joined at:", 
                value = member.joined_at.strftime("%d %B %Y %H:%M:%S"),
                inline = False
            )
        
            action.set_thumbnail(url = member.avatar_url)

            await member.add_roles(role)
            await logger.LogAction(self.client, action)      
        except:
            print("Error while adding role on join")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            action = discord.Embed(
                title = 'Member left',
                colour = discord.Colour.red()
            )
         
            action.add_field(
                name = "Member", 
                value = member.mention + ' ' + member.name + '#' + member.discriminator,
                inline = False
            )
        
            action.add_field(
                name = "Member registered at:", 
                value = member.created_at.strftime("%d %B %Y %H:%M:%S"),
                inline = False
            )
        
            action.add_field(
                name = "Member joined at:", 
                value = member.joined_at.strftime("%d %B %Y %H:%M:%S"),
                inline = False
            )

            action.add_field(
                name = "Member leafet at:",
                value = str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")),
                inline = False                              
            )
        
            action.set_thumbnail(url = member.avatar_url)
        
            await logger.LogAction(self.client, action)

            try:
                user = self.session.query(User) \
                    .filter(User.UserId == member.id) \
                    .one()
                
                user.DiscordStatus = "Kicked"
                self.session.commit()
                self.session.close()
            except SQLAlchemyError as err:
                print(str(err))
                
                
        except:
            print("Error")
   
    @commands.Cog.listener()
    async def on_member_update(self, before, after):

        # Roles removed
        if before.roles < after.roles:
            action = discord.Embed(
                title = 'Role removed',
                colour = discord.Colour.green()
            )

            action.add_field(
                name = "Member:", 
                value = after.mention + ' ' + after.name + '#' + after.discriminator,
                inline = False
            )

            roleSet = set(before.roles) - set(after.roles)
            roles = []
            for role in roleSet:
                action.add_field(
                    name = "Role:",
                    value = role.mention
                )

                action.add_field(
                    name = "Time:",
                    value = str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")),
                    inline = False
                )
                
                action.set_thumbnail(url = before.avatar_url)
                await logger.LogAction(self.client, action)

                try:
                    removedRole = self.session.query(Role) \
                        .filter(Role.RoleId == role.id) \
                        .one()

                    user = self.session.query(User) \
                        .filter(User.UserId == before.id) \
                        .one()
                    
                    user.Roles.remove(removedRole)
                    self.session.commit()
                    self.session.close()
                except SQLAlchemyError as err:
                    print(str(err))
                    

        # Role added           
        elif before.roles > after.roles:
            action = discord.Embed(
                title = 'Role added',
                colour = discord.Colour.green()
            )

            action.add_field(
                name = "Member:", 
                value = after.mention + ' ' + after.name + '#' + after.discriminator,
                inline = False
            )

            roleSet = set(after.roles) - set(before.roles)
            for role in roleSet:
                
                action.add_field(
                    name = "Role:",
                    value = role.mention
                )

                action.add_field(
                    name = "Time:",
                    value = str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")),
                    inline = False
                )
                
                action.set_thumbnail(url = before.avatar_url)

                await logger.LogAction(self.client, action)
                
                try:
                    ddedRole = self.session.query(Role) \
                        .filter(Role.RoleId == role.id) \
                        .one()
                    
                    user = self.session.query(User) \
                        .filter(User.UserId == before.id) \
                        .one()

                    user.Roles.append(addedRole)
                    self.session.commit()
                    self.session.close()
                except SQLAlchemyError as err:
                    print(str(err))

                
        if before.nick != after.nick:
            action = discord.Embed(
                title = "Name changed",
                colour = discord.Colour.green()
            )

            action.add_field(
                name = "Member:",
                value = after.mention + ' ' + after.name + '#' + after.discriminator,
                inline = False
            )

            action.add_field(
                name = "Old name:",
                value = before.nick,
                inline = False
            )

            action.add_field(
                name = "New name:",
                value = after.nick,
                inline = False
            )

            action.add_field(
                name = "Time:",
                value = str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S")),
                inline = False
            )

            action.set_thumbnail(url = before.avatar_url)

            await logger.LogAction(self.client, action)
            
            try:
                user = self.session.query(User) \
                    .filter(User.UserId == after.id) \
                    .one()
                
                user.Name = after.nick
                self.session.commit()
                self.session.close()
            except SQLAlchemyError as err:
                print(str(err))
                


    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            try:
                user = self.session.query(User) \
                    .filter(User.UserId == after.id) \
                    .one()
                
                user.Username = after.name
                self.session.commit()
                self.session.close()
            except SQLAlchemyError as err:
                print(str(err))
                
        
        if before.discriminator != after.discriminator:
            try:
                user = self.session.query(User) \
                    .filter(User.UserId == after.id) \
                    .one()
                
                user.Discriminator = after.discriminator
                self.session.commit()
                self.session.close()
            except SQLAlchemyError as err:
                print(str(err))
                

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.content.startswith("$purge"):
            return

        action = discord.Embed(
            title = "Message deleted",
            colour = discord.Colour.red().value
        )
        action.set_thumbnail(url = message.author.avatar_url)
        action.add_field(
            name = "Author:",
            value = message.author.mention,
            inline = False
        )

        action.add_field(
            name = "Channel:",
            value = message.channel.mention,
            inline = False
        )

        action.add_field(
            name = "Content:",
            value = message.content,
            inline = False
        )

        action.add_field(
            name = "Created at:",
            value = str(message.created_at.strftime("%d %B %Y %H:%M:%S")),
            inline = False
        )
        

        await logger.LogAction(self.client, action)


def setup(client):
    client.add_cog(Events(client))