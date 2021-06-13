import discord
from discord.ext import commands

import os
from pathlib import Path

from dotenv import load_dotenv

import json

def main():
    load_dotenv()

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = '$', intents = intents)
    bot.remove_command('help')

    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            try:
                filename = Path(file).stem
                cog = f"cogs.{filename}"
                bot.load_extension(cog)  
            except Exception as error:
                print(file + ": Error - " + str(error))

    DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    main()
