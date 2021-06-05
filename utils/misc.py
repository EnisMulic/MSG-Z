import discord

def get_channel_id(client, channelName):
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name == channelName:
                return channel.id

def get_member(client, member_id):
    for guild in client.guilds:
        return guild.get_member(member_id)

def get_role_by_name(client, roleName):
    for guild in client.guilds:
        for role in guild.roles:
            if role.name == roleName:
                return role

def get_role_by_id(client, roleId):
    for guild in client.guilds:
        for role in guild.roles:
            if role.id == roleId:
                return role