import discord
from discord.ext import commands

import datetime
import os

from utils import misc
from utils import logger
from utils.google_drive import main

import json

class Backup(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open('.\\config.json', "r", encoding="utf-8") as json_for_url:
            data = json.load(json_for_url)
        self.folders = data["Google-Drive"]

    def is_mod(self, user_roles):
        return "Administrator" in user_roles or "Moderator" in user_roles
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        if reaction.emoji.name == "📌":
            user = misc.getMember(self.client, reaction.user_id)
            if self.is_mod([role.name for role in user.roles]):
                channel = self.client.get_channel(reaction.channel_id)
                message = await channel.fetch_message(reaction.message_id)
                
                files = []
                for attachment in message.attachments:
                    file = await attachment.to_file()
                    files.append(file)
                    filePath = "./payload/" + attachment.filename
                    await attachment.save(filePath)
                    main.uploadFile(attachment.filename, filePath, self.folders[channel.name])
                    os.remove(filePath)

                await self.LogBackup(user, channel)

    async def LogBackup(self, member, channel):
        

        action = discord.Embed(
            title = 'File(s) backed up to google drive',
            colour = discord.Colour.green()
        )
        
        action.add_field(
            name = "By Admin/Mod", 
            value = member.mention + ' ' + member.name + '#' + member.discriminator,
            inline = False
        )

        action.add_field(
            name = "In channel:", 
            value = channel.mention,
            inline = False
        )
    
        action.set_footer(
            text = str(datetime.datetime.now().strftime("%d %B %Y %H:%M:%S"))
        )
    
        
    
        action.set_thumbnail(url = member.avatar_url)

        await logger.LogAction(self.client, action)

def setup(client):
    client.add_cog(Backup(client))