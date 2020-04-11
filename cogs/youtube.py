import discord
from discord.ext import commands, tasks

import requests
from bs4 import BeautifulSoup

import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError

import datetime
import json

import models.youtube as yt
from models.user import User
import models.base as base

from utils import misc


class Youtube(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.session = base.Session()
        
        self.youtube_url = 'https://www.youtube.com/watch?v='
        self.youtube_rss = "https://www.youtube.com/feeds/videos.xml?channel_id="

        self.get_videos()
    
    def _get_channels(self, session):
        try:
            return self.session.query(yt.Youtube) \
                .filter(yt.Youtube.Output == True) \
                .all()
        except SQLAlchemyError as err:
            print(str(err))
            


    def get_videos_for_channel(self, channel_id):

        response = requests.get(self.youtube_rss + channel_id)
        response = BeautifulSoup(response.text, "lxml")

        video_data = response.select("entry")
        videos = []

        for video in video_data:
            videoId = video.find("yt:videoid")
            title = video.find("title")
            published = video.find("published")

            published_date = published.text[:10]
            published_time = published.text[11:19]

            videos.append([videoId.text, title.text, published_date + " " + published_time])


        return videos


    @commands.command(aliases=["youtube"])
    async def get_channels(self, ctx, *, search: str = ''):
        try:
            channels = self.session.query(yt.Youtube) \
                        .filter(yt.Youtube.ChannelName.ilike(f"%{search}%"))

            description = '\n'
            for channel in channels:
                mark = ":white_check_mark:" if channel.Output else ":negative_squared_cross_mark:"
                description += f"{mark} | [{channel.ChannelName}](https://www.youtube.com/channel/{channel.ChannelId})\n\n"
                              
            embed = discord.Embed(
                title = "Youtube",
                description = description,
                colour = discord.Colour.red()
            ) 
            
            await ctx.send(embed = embed)
        except SQLAlchemyError as err:
            await ctx.send(str(err))

    @commands.command(aliases=["remove-channel"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def remove_channel(self, ctx, channel_id: str):
        try:
            channel = self.session.query(yt.Youtube) \
                        .filter(yt.Youtube.ChannelId == channel_id) \
                        .one()
        
            self.session.delete(channel)
            self.session.commit()
        except SQLAlchemyError as err:
            await ctx.send(str(err))
    
    @commands.command(aliases=["add-channel"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def add_channel(self, ctx, channel_id: str, *channel_name: str, member: discord.Member = None):
        videos = self.get_videos_for_channel(channel_id)
        channel_name = ' '.join(channel_name)
        
        try:
            if videos: 
                video_id = videos[0][0]
                video_title = videos[0][1]
                video_timestamp = datetime.datetime.strptime(videos[0][2], "%Y-%m-%d %H:%M:%S")
            else:
                video_id = ""
                video_title = ""
                video_timestamp = datetime.datetime.strptime("1970-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
                
            newChannel = yt.Youtube(channel_id, channel_name, video_id, video_title, video_timestamp, member)
            self.session.add(newChannel)
            self.session.commit()
        
        except SQLAlchemyError as err:
            print(str(err))

    @commands.command(aliases=["link-channel"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def link_channel(self, ctx, member: discord.Member, channel_id: str):
        try:
            user = self.session.query(User) \
                    .filter(User.UserId == member.id) \
                    .one()
            
            channel = self.session.query(yt.Youtube) \
                        .filter(yt.Youtube.ChannelId == channel_id) \
                        .one()
        
            channel.UserId = user.UserId
        
            self.session.commit()
            self.session.close()
        except SQLAlchemyError as err:
            await ctx.send(str(err))
            
            
    @commands.command(aliases=["toggle-channel"])
    @commands.has_any_role('Administrator', 'Moderator')
    async def toggle_channel(self, ctx, *, channel_name: str):
        try:
            channel = self.session.query(yt.Youtube) \
                        .filter(yt.Youtube.ChannelName == channel_name) \
                        .one()
        
            if channel is not None:
                channel.Output = not channel.Output
            
            self.session.commit()
        except Exception as err:
            await ctx.send(str(err))
    
    def get_videos(self):
        try:
            self.send_videos.start()
        
        except Exception as err:
            print(str(err))
            self.get_videos()

    @tasks.loop(minutes = 15)
    async def send_videos(self):
        print("Scraping Youtube...")


        youtube_channels = self._get_channels(session)
        discord_channel = self.client.get_channel(misc.getChannelID(self.client, "youtube"))
        
        
        for youtube_channel in youtube_channels:
            videos = self.get_videos_for_channel(youtube_channel.ChannelId)
            
            videos = videos[::-1]
            for video in videos:
                

                if str(youtube_channel.Published) < video[2] and video[0] != youtube_channel.VideoId:
                    await discord_channel.send(self.youtube_url + video[0])

                    youtube_channel.VideoId = video[0]
                    youtube_channel.VideoTitle = video[1]
                    youtube_channel.Published = datetime.datetime.strptime(video[2], "%Y-%m-%d %H:%M:%S")
                    
                    self.session.commit()

                            
    def cog_unload(self):
        self.send_videos.cancel()

    @send_videos.before_loop
    async def before_send_videos(self):
        print('Youtube RSS: Waiting...')
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Youtube(client))
