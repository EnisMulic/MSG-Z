import discord

from . import misc

async def LogAction(client, embed):
    channel = client.get_channel(misc.getChannelID(client, 'logger'))
    await channel.send(embed = embed)
    