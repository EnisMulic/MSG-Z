import discord
from discord.ext import commands

from cogs.utils import logger

class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            role = discord.utils.get(member.guild.roles, name="A New Contender")
            action = discord.Embed(
                title = 'Member Joined',
                colour = discord.Colour.green().value
            )
         
            action.add_filed(
                name = "Member", 
                value = member.mention + ' ' + member.name + '#' + member.discriminator,
                inline = False
            )
        
            actipn.add_filed(
                name = "Member registered at:", 
                value = member.created_at.strftime("%d %B %Y %H:%M:%S"),
                inline = False
            )
        
            action.add_field(
                name = "Member joined at:", 
                value = member.joined_at.strftime("%d %B %Y %H:%M:%S"),
                inline = False
            )
        
            action.set_thumbnail(url = member.avatar_url)
        
            await logger.LogAction(self.client, action)
            await member.add_roles(role)
                
                
        except:
            print("Error while adding role on join")


   
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
            
        if before.roles < after.roles:
            print("Role removed")
            print(set(before.roles) - set(after.roles))
        elif before.roles > after.roles:
            print("Role added")
            print(set(after.roles) - set(before.roles))
        
            
        
        # if before.nick != after.nick:
        #     action = discord.Embed({
        #         "title": "Name changed",
        #         "colour": int(discord.Colour.green().value),
        #         "thumbnail": {"url": str(before.avatar_url)},
        #         "fields": [
        #             {
        #                 "inline": False,
        #                 "name": "Member",
        #                 "value": after.mention + ' ' + after.name + '#' + after.discriminator
        #             },
        #             {
        #                 "inline": False,
        #                 "name": "Old name",
        #                 "value": before.nick
        #             },
        #             {
        #                 "inline": False,
        #                 "name": "New name",
        #                 "value": after.nick
        #             },
        #             {
        #                 "inline": False,
        #                 "name": "Time",
        #                 "value": str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S"))
        #             }]
        #     })
        #     await self.logger.LogAction(action)

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            print("User has changed their name")
            #update database
        
        if before.discriminator != after.discriminator:
            print("User has changed their discriminator")
            #update database

def setup(client):
    client.add_cog(Events(client))