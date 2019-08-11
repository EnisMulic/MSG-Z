import discord
from discord.ext import commands

import datetime

class Members(commands.Cog):
    def __init__(self, client):
        self.client = client

    def getChannelID(self, channelName):
        for guild in self.client.guilds:
            for channel in guild.channels:
                if channel.name == channelName:
                    return channel.id   

        
    async def LogAction(self, embed):
        channel = self.client.get_channel(self.getChannelID('logger'))
        await channel.send(embed = embed)
        
    
    @commands.command(aliases=["add-role"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_role(self, ctx, member: discord.Member, *roles: discord.Role):#test this
        newRolesList = []
        for role in roles:
            newRole = discord.utils.get(member.guild.roles, name=str(role))
            if newRole not in member.roles:
                newRolesList += [newRole.mention]
                await member.add_roles(newRole)
            else:
                await ctx.send(member.nick + ' vec ima ulogu ' + newRole.name)
        
            
        action = discord.Embed(
            title = "Add Role",
            colour = discord.Colour.green().value
        )
        
        action.add_field(
            name = "Member",
            value = member.mention + ' ' + member.name + '#' + member.discriminator,
           inline = False
        )
        
        action.add_field(
            name = "Roles",
            value = '\n'.join(newRolesList),
            inline = False
        )
        
        action.add_field(
            name = "Time",
            value = datetime.datetime.now().strftime("%d %B %Y %H:%M:%S"),
            inline = False
        )
        
        action.set_thumbnail(url = member.avatar_url)
        
        await self.LogAction(action)
        
        
    @commands.command(aliases=["remove-role"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_role(self, ctx, member: discord.Member, *roles: discord.Role):
        for role in roles:
            oldRole = discord.utils.get(member.guild.roles, name=str(role))
            if oldRole in member.roles:
                action = discord.Embed().from_dict({
                    "title": "Role removed",
                    "colour": int(discord.Colour.green().value),
                    "thumbnail": {"url": str(member.avatar_url)},                       
                    "fields": [
                        {
                            "inline": False, 
                            "name": "Member", 
                            "value": member.mention + ' ' + member.name + '#' + member.discriminator
                        },
                        {
                            "inline": False, 
                            "name": "Role",  
                            "value": oldRole.mention
                        },
                        {
                            "inline": False, 
                            "name": "Time", 
                            "value": str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S"))
                        }]
                })
                await self.LogAction(action)
                await member.remove_roles(oldRole)   
            else:
                await ctx.send(member.nick + ' nema ulogu ' + oldRole.name)
        
        
    @commands.command(aliases=["set-name"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def set_name(self, ctx, member: discord.Member, *nick):
        newName = ' '.join(nick)
        await member.edit(nick = newName)
            
    
    #new cog ???
    @commands.command()
    @commands.has_any_role('Administrator', 'Moderator')
    async def purge(self, ctx, numberOfMessages = 1):
        await ctx.channel.purge(limit = int(numberOfMessages + 1))
        #log
        
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
        
            await LogAction(action)
            await member.add_roles(role)
                
                
        except:
            print("Error while adding role on join")
            
    #on_member_update
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
            
        if before.roles < after.roles:
            print("Role removed")
            print(set(before.roles) - set(after.roles))
        elif before.roles > after.roles:
            print("Role added")
            print(set(after.roles) - set(before.roles))
        
            
        
        #if before.nick != after.nick:
            # action = discord.Embed({
            #     "title": "Name changed",
            #     "colour": int(discord.Colour.green().value),
            #     "thumbnail": {"url": str(before.avatar_url)},
            #     "fields": [
            #         {
            #             "inline": False,
            #             "name": "Member",
            #             "value": after.mention + ' ' + after.name + '#' + after.discriminator
            #         },
            #         {
            #             "inline": False,
            #             "name": "Old name",
            #             "value": before.nick
            #         },
            #         {
            #             "inline": False,
            #             "name": "New name",
            #             "value": after.nick
            #         },
            #         {
            #             "inline": False,
            #             "name": "Time",
            #             "value": str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S"))
            #         }]
            # })
            # await self.LogAction(action)
        
        
    #on_user_update
    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            print("User has changed their name")
            #update database
        
        if before.discriminator != after.discriminator:
            print("User has changed their discriminator")
            #update database
            
    
def setup(client):
    client.add_cog(Members(client))