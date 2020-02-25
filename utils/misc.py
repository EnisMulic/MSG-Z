import discord

def getChannelID(client, channelName):
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name == channelName:
                return channel.id

def getMember(client, member_id):
    for guild in client.guilds:
        for member in guild.members:
            if member.id == member_id:
                return member

def getRoleId(client, roleName):
    for guild in client.guilds:
        for role in guild.rolse:
            if role.name == roleName:
                return role.id