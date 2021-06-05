from utils import misc
from constants import channels

async def log_action(client, embed):
    channel = client.get_channel(misc.getChannelID(client, channels.LOGGER))
    await channel.send(embed = embed)

async def log_action_raw(client, content, files):
    channel = client.get_channel(misc.getChannelID(client, channels.LOGGER))
    await channel.send(content = content, files = files)
    