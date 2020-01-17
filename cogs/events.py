import discord
from discord.ext import commands

import datetime

from utils import logger
from models.user import User
from sqlalchemy.exc import SQLAlchemyError
from models.role import Role

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

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
            database = self.client.get_cog('Database')
            if database is not None:
                try:
                    session = database.Session()
                    user = session.query(User) \
                            .filter(User.UserId == member.id) \
                            .one()
                    
                    user.DiscordStatus = "Kicked"
                    session.commit()
                    session.close()
                except SQLAlchemyError as err:
                    print(str(err))
                
        except:
            print("Error")
   
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        database = self.client.get_cog('Database')

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

                if database is not None:
                    session = database.Session()
                    removedRole = session.query(Role) \
                                    .filter(Role.RoleId == role.id) \
                                    .one()

                    user = session.query(User) \
                                .filter(User.UserId == before.id) \
                                .one()
                    
                    user.Roles.remove(removedRole)
                    session.commit()
                    session.close()

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
                if database is not None:
                    session = database.Session()
                    addedRole = session.query(Role) \
                                    .filter(Role.RoleId == role.id) \
                                    .one()
                    
                    user = session.query(User) \
                                .filter(User.UserId == before.id) \
                                .one()

                    user.Roles.append(addedRole)
                    session.commit()
                    session.close()
                
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
            if database is not None:
                # await database.change_member_name(after, after.nick)
                try:
                    session = database.Session()
                    user = session.query(User) \
                            .filter(User.UserId == after.id) \
                            .one()
                    
                    user.Name = after.nick
                    session.commit()
                    session.close()
                except SQLAlchemyError as err:
                    print(str(err))


    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            database = self.client.get_cog('Database')
            if database is not None:
                # await database.change_member_username(after)
                try:
                    session = database.Session()
                    user = session.query(User) \
                            .filter(User.UserId == after.id) \
                            .one()
                    
                    user.Username = after.name
                    session.commit()
                    session.close()
                except SQLAlchemyError as err:
                    print(str(err))
        
        if before.discriminator != after.discriminator:
            database = self.client.get_cog('Database')
            if database is not None:
                # await database.change_member_discriminator(after)
                try:
                    session = database.Session()
                    user = session.query(User) \
                            .filter(User.UserId == after.id) \
                            .one()
                    
                    user.Discriminator = after.discriminator
                    session.commit()
                    session.close()
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
        action.set_thumbnail(url = self.client.user.avatar_url)
        action.add_field(
            name = "Author:",
            value = message.author.mention + ' ' + message.author.name + '#' + message.author.discriminator,
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