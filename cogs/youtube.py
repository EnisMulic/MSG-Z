import discord
from discord.ext import commands
from discord.ext import tasks

import requests
import json
from bs4 import BeautifulSoup

import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import models.youtube as yt

from utils import misc


class Youtube(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.base_search_url = 'https://www.youtube.com/channel/{}/videos'
        self.youtube_url = 'https://www.youtube.com'

        self.get_videos()
    
    def get_channels(self):
        database = self.client.get_cog('Database')
        if database is not None:
            return database.session.query(yt.Youtube).all()
            # database.cursor.execute('SELECT * FROM Youtube')
            # channels = database.cursor.fetchall()

            # return channels



    def get_videos_for_channel(self, channel_id):

        response = requests.get(self.base_search_url.format(channel_id))
        response = BeautifulSoup(response.text, "html.parser")

        video_data = response.select("a.yt-uix-tile-link")
        videos = []

        for video in video_data:
            title = video.get("title")
            videoId = video.get("href")
            videos.append([title, videoId])

        return videos

    @commands.command(aliases=["get-channels"])
    async def _get_channels(self, ctx):
        database = self.client.get_cog('Database')
        if database is not None:
            #database.cursor.execute('SELECT * FROM Youtube')
            #channels = database.cursor.fetchall()
            session = database.Session()
            channels = session.query(yt.Youtube).all()

            for channel in channels:
                await ctx.send(channel.ChannelName + ": " + "https://www.youtube.com/channel/" + channel.ChannelId)

            session.close()

    @commands.command(aliases=["remove-channel"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_channel(self, ctx, channel_id: str):
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                channel = database.session.query(yt.Youtube) \
                            .filter(yt.Youtube.ChannelId == channel_id) \
                            .one()
                database.session.delete(channel)
                database.session.commit()

                database.cursor.execute('DELETE FROM Youtube WHERE ChannelID = "{}";'.format(channel_id,))
                database.db.commit()
            except:
                print("Procedure Remove Channel: Something went wrong:")
    
    @commands.command(aliases=["add-channel"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_channel(self, ctx, channel_id: str, *channel_name: str, member: discord.Member = None):
        videos = self.get_videos_for_channel(channel_id)
        channel_name = ' '.join(channel_name)
        database = self.client.get_cog('Database')
        if database is not None:
            try:
                if videos:
                    video_id = videos[0][1]
                    video_title = videos[0][0]
                else:
                    video_id = ""
                    video_title = ""

                newChannel = yt.Youtube(channel_id, channel_name, video_id, video_title, member)
                database.session.add(newChannel)
                database.session.commit()
            except SQLAlchemyError as err:
                print(str(err))


    def get_videos(self):
        try:
            self.send_videos.start()
        
        except Exception as err:
            print(str(err))
            self.get_videos()

    @tasks.loop(minutes = 15)
    async def send_videos(self):
        print("Scraping Youtube...")
        youtube_channels = self.get_channels()
        discord_channel = self.client.get_channel(misc.getChannelID(self.client, "youtube"))
        database = self.client.get_cog("Database")

        for youtube_channel in youtube_channels:
            videos = self.get_videos_for_channel(youtube_channel.ChannelId)
            for video in videos:
                print("Link " + video[1] + " | " + youtube_channel.VideoId)
                if video[1] == youtube_channel.VideoId:
                    break
                else:
                    await discord_channel.send(self.youtube_url + video[1])

                    if database is not None:
                        channel = database.session.query(yt.Youtube) \
                                    .filter(yt.Youtube.ChannelId == youtube_channel.ChannelId) \
                                    .one()
                        channel.VideoId = video[0][1]
                        channel.VideoTitle = video[0][0]

                        database.session.commit()
                        #await database.update_youtube_channel_info(youtube_channel[0], video)

    
    def cog_unload(self):
        self.send_videos.cancel()

    @send_videos.before_loop
    async def before_send_videos(self):
        print('Youtube API: Waiting...')
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Youtube(client))