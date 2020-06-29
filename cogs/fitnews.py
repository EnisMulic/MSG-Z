import discord
from discord.ext import commands
from discord.ext import tasks

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from datetime import datetime

from utils import notifications
from utils import misc
import json

class FitNews(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = 'https://fit.ba/news'
        self.get_notifications()

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def main(self):
        print("Scraping FIT News...")

        try:
            async with aiohttp.ClientSession() as session:
                html = await self.fetch(session, self.url)
                response = BeautifulSoup(html, "html.parser")
                news = response.select("li.media")
            
            notifications_list = []
            for new in news:
                link = 'https://fit.ba/' + new.find("a", {"class": "cover"}).get("href")
                meta = new.find("small").text
                date = re.search(r'\d{2}.\d{2}.\d{4}', meta)
                time = re.search(r'\d{2}:\d{2}', meta)
                author = meta.split() 

                notifications_list.append(
                    notifications.DLWMS_Notification(
                        link, "", date.group() + " " + time.group(), "", author[1] + " " + author[2], ""
                    )
                )

            last_notification_json = {}
        
            with open(".\\last_notification_fit_news.json", "r", encoding="utf-8") as jsonDataFile:
                last_notification_json = json.load(jsonDataFile)

            last_notification = notifications.DLWMS_Notification(
                last_notification_json["link"],
                last_notification_json["title"],
                last_notification_json["date"],
                last_notification_json["subject"],
                last_notification_json["author"],
                last_notification_json["content"]
            )

            lastSent = last_notification
            notifications_list.reverse()

            for notification in notifications_list or []:
                if notification > last_notification and notification.link != last_notification.link:
                    channel = self.client.get_channel(misc.getChannelID(self.client, "logger"))
                    if channel is not None:
                        await channel.send(notification.link)
                    lastSent = notification

            if lastSent != last_notification:
                with open(".\\last_notification_fit_news.json", "w", encoding="utf-8") as jsonDataFile:
                    json.dump(lastSent.__dict__, jsonDataFile, indent = 4)
            
        except Exception as err:
            print("Error: " + str(err))
            
            

    @tasks.loop(minutes = 1)
    async def send_notifications(self):
        await self.main()
        
    def cog_unload(self):
        self.send_notifications.cancel()
        

    def get_notifications(self):
        try:
            self.send_notifications.start()
        
        except Exception as err:
            print(str(err))
            self.get_notifications()

    @send_notifications.before_loop
    async def before_send_notifications(self):
        print('Scraper - Fit News: Waiting...')
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(FitNews(client))