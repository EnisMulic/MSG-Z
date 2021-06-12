import discord
from discord.ext import commands

import json

def get_token():
    with open("config.json", encoding='utf-8') as json_data_file:
        data = json.load(json_data_file)
    return data["Discord"]["Token"]

def main():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = '$', intents = intents)

    token = get_token()

    bot.run(token)

if __name__ == '__main__':
    main()
