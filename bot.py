import discord
from discord.ext import commands

import asyncio
import json
import os
import sys


client = commands.Bot(command_prefix = '$')
client.remove_command('help')

def getToken():
    with open("config.json", encoding='utf-8') as json_data_file:
        data = json.load(json_data_file)
    return data["Discord"]["Token"]

cogsDir = ".\\cogs"
#

if __name__ == '__main__':
    

    @client.event
    async def on_ready():
        print("Running on: " + discord.__version__)
        await client.change_presence(activity = discord.Activity(name = "FIT DLWMS & Youtube", type = 3))

    

    for file in os.listdir(cogsDir):
        if file.endswith(".py"):
            try:
                file = f"cogs.{file.replace('.py', '')}"
                client.load_extension(file)  
            except Exception as error:
                print(file + ": Error - " + str(error))
                
    
    
    client.run(getToken())
    
