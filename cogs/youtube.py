import discord
from discord.ext import commands
from discord.ext import tasks

import requests
import json
from bs4 import BeautifulSoup

from utils import misc


class Youtube(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open(".\\config.json") as json_for_api:
            data = json.load(json_for_api)
        self.api_key = data["Youtube-API-Key"]

        self.base_search_url = 'https://www.googleapis.com/youtube/v3/search?'
        self.youtube_url = 'https://www.youtube.com/watch?v='

        self.get_videos()
    
    def get_channels(self):
        database = self.client.get_cog('Database')
        if database is not None:
            database.cursor.execute('SELECT * FROM Youtube')
            channels = database.cursor.fetchall()

            return channels

    def get_videos_for_channel(self, channel_id):
        first_url = self.base_search_url + \
            'key={}&channelId={}&part=snippet,id&order=date&maxResults=25'.format(self.api_key, channel_id)

        response = requests.get(first_url)
        return json.loads(response.text)
        
    
    @commands.command(aliases=["add-channel"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_channel(self, ctx, channel_id: str):
        videos = self.get_videos_for_channel(channel_id)
        
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                database.cursor.execute('INSERT INTO Youtube(\
                                            ChannelID,\
                                            ChannelName,\
                                            Title,\
                                            PublishedAt,\
                                            VideoID\
                                        )\
                                        VALUES(\
                                            "{}",\
                                            "{}",\
                                            "{}",\
                                            "{}",\
                                            "{}"\
                                        );'.format(
                                            channel_id,
                                            videos["items"][0]["snippet"]["channelTitle"],
                                            videos["items"][0]["snippet"]["title"],
                                            videos["items"][0]["snippet"]["publishedAt"][:10],
                                            videos["items"][0]["id"]["videoId"]
                                        ))
                database.db.commit()
            except:
                print("Procedure Insert Channel: Something went wrong:")

    def get_videos(self):
        try:
            self.send_videos.start()
        
        except Exception as err:
            print(str(err))
            self.get_videos()

    @tasks.loop(minutes = 15)
    async def send_videos(self):
        youtube_channels = self.get_channels()
        discord_channel = self.client.get_channel(misc.getChannelID(self.client, "youtube"))
        database = self.client.get_cog("Database")

        for youtube_channel in youtube_channels:
            videos = self.get_videos_for_channel(youtube_channel[0])
            
            for video in videos["items"]:
                if video["snippet"]["publishedAt"][:10] >= youtube_channel[3] and \
                   video["id"]["videoId"] != youtube_channel[4]:
                   
                   await discord_channel.send(self.youtube_url + video["id"]["videoId"])

                   if database is not None:
                       await database.update_youtube_channel_info(video)

    
    def cog_unload(self):
        self.send_videos.cancel()

    @send_videos.before_loop
    async def before_send_videos(self):
        print('Youtube API: Waiting...')
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Youtube(client))