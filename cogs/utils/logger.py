import discord

from . import miscellaneous

async def LogAction(client, embed):
    channel = client.get_channel(miscellaneous.getChannelID(client, 'logger'))
    await channel.send(embed = embed)
        