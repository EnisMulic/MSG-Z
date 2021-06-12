import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

import json

def main():
    load_dotenv()

    

    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = '$', intents = intents)

    DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

    bot.run(DISCORD_TOKEN)

if __name__ == '__main__':
    main()
