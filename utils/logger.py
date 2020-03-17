import discord

from utils import misc

async def LogAction(client, embed):
    channel = client.get_channel(misc.getChannelID(client, 'logger'))
    await channel.send(embed = embed)

async def LogActionRaw(client, content, files):
    channel = client.get_channel(misc.getChannelID(client, 'logger'))
    await channel.send(content = content, files = files)
    