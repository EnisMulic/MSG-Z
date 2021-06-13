import discord
from constants import channels

async def log_action(guild, embed):
    channel = discord.utils.get(guild.text_channels, name=channels.LOGGER)
    await channel.send(embed = embed)