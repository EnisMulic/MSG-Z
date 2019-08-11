import discord
from discord.ext import commands
import asyncio
import json
import datetime
import os
import sys

from notifications import Discord_Bot_Notification

client = commands.Bot(command_prefix = '!')

def getToken():
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)
    return data["Discord"]["Token"]

initial_extensions = ['members']
cogsDir = "cogs"

if __name__ == '__main__':
    for file in os.listdir(".\\cogs"):
        try:
            if os.path.isfile(file):
                file = f"cogs.{file.replace('.py', '')}"
                client.load_extension(file)
                print("Success")
        except Exception as error:
            print(file + ": Error - " + str(error))
            raise error
    
    client.run(getToken())
