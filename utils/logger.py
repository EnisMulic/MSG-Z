import discord

import os

from constants import channels


async def log_action(guild, embed):
    channel = discord.utils.get(guild.text_channels, name = channels.LOGGER)
    await channel.send(embed = embed)


async def log_to_guild(bot, embed):
    GUILD_NAME = os.environ.get("GUILD_NAME")

    channel = discord.utils.get(bot.get_all_channels(), guild__name = GUILD_NAME, name = channels.LOGGER)
    await channel.send(embed = embed)
