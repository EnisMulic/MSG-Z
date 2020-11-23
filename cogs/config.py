import discord
from discord.ext import commands
from discord.ext import tasks

import json

class Config(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_any_role('Administrator')
    async def config(self, ctx, cog, key, value):
        cog_config = {}
        with open(f".\\config\{cog}.json", "r", encoding="utf-8") as jsonConfigFile:
            cog_config = json.load(jsonConfigFile)

        if key in cog_config:
            cog_config[key] = value

            with open(f".\\config\{cog}.json", "w", encoding="utf-8") as jsonConfigFile:
                json.dump(cog_config, jsonConfigFile, indent = 4)
        

      

def setup(client):
    client.add_cog(Config(client))