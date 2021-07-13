import discord
from discord.ext import commands, tasks

import os
import json
import hashlib

from models.news import News
import models.base as base

from constants import channels
from scrapers import fitba, dlwms

class Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = base.Session()

        with open("./config/dlwms.json", "r", encoding="utf-8") as json_config_file:
            self.subjects = json.load(json_config_file)["subjects"]

        self.fitba_scraper = fitba.FitBaScraper()
        self.scrape_fitba.start()

        self.dlwms_scraper = dlwms.DLWMSScraper()
        self.scrape_dlwms.start()

    @tasks.loop(minutes=1)
    async def scrape_dlwms(self):
        GUILD_NAME = os.environ.get("GUILD_NAME")

        news = [i async for i in self.dlwms_scraper.parse_data()]
        for new in news:
            try:
                notification = News(
                    url = hashlib.md5(new["url"].encode('utf-8')).hexdigest(),
                    dateTime = new["date"], 
                    source = "dlwms"
                )

                self.session.add(notification)
                self.session.commit()

                embed = discord.Embed(title = new['title'], url = new['url'], colour = discord.Colour.blue().value)
                embed.set_author(name = GUILD_NAME, url = self.bot.user.avatar_url, icon_url = self.bot.user.avatar_url)
                embed.add_field(name = "Obavijest", value = new['content'], inline = False)
                embed.set_footer(text = f"Datum i vrijeme: {new['date']} • Autor: {new['author']}")

                try:
                    channelName = self.subjects[new["subject"]]
                except:
                    channelName = "obavijesti"
                
                channel = discord.utils.get(self.bot.get_all_channels(), guild__name=GUILD_NAME, name=channelName)
                if channel is not None:
                    await channel.send(embed = embed)
            except:
                pass

    @scrape_dlwms.before_loop
    async def before_scrape_fitba(self):
        print('Scraper - Fit DLWMS: Waiting...')
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=30)
    async def scrape_fitba(self):
        GUILD_NAME = os.environ.get("GUILD_NAME")
        channel = discord.utils.get(self.bot.get_all_channels(), guild__name=GUILD_NAME, name=channels.OBAVIJESTI)

        news = [i async for i in self.fitba_scraper.parse_data()]
        for new in news:
            if channel is not None:
                try:
                    notification = News(
                        url = hashlib.md5(new["url"].encode('utf-8')).hexdigest(),
                        dateTime = new["date"], 
                        source = "fitba"
                    )

                    self.session.add(notification)
                    self.session.commit()

                    await channel.send(new["url"])
                except:
                    pass

    @scrape_fitba.before_loop
    async def before_scrape_fitba(self):
        print('Scraper - Fit News: Waiting...')
        await self.bot.wait_until_ready()
    
def setup(bot):
    bot.add_cog(Scraper(bot))