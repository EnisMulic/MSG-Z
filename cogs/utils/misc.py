import discord

def getChannelID(client, channelName):
        for guild in client.guilds:
            for channel in guild.channels:
                if channel.name == channelName:
                    return channel.id