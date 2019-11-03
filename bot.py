import discord
from discord.ext import commands

import asyncio
import json
import os
import sys


client = commands.Bot(command_prefix = '$')

def getToken():
    with open("config.json") as json_data_file:
        data = json.load(json_data_file)
    return data["Discord"]["Token"]

cogsDir = ".\\cogs"

if __name__ == '__main__':
    @client.event
    async def on_ready():
        print("3, 4, SAD!")
        await client.change_presence(activity = discord.Game(name = "In development"))


    for file in os.listdir(cogsDir):
        if file.endswith(".py"):
            try:
                file = f"cogs.{file.replace('.py', '')}"
                client.load_extension(file)  
            except Exception as error:
                print(file + ": Error - " + str(error))
                
    
    
    client.run(getToken())
    
