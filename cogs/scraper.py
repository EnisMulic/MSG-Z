import discord
from discord.ext import commands, tasks

import os

from constants import channels
from scrapers import fitba
from utils import logger

class Scraper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.fitba_scraper = fitba.FitBaScraper()
        self.scrape_fitba.start()

    @tasks.loop(minutes=1)
    async def scrape_dlwms(self):
        pass

    @tasks.loop(minutes=30)
    async def scrape_fitba(self):
        GUILD_NAME = os.environ.get("GUILD_NAME")
        channel = discord.utils.get(self.bot.get_all_channels(), guild__name=GUILD_NAME, name=channels.OBAVIJESTI)

        news = [i async for i in self.fitba_scraper.parse_data()]
        for new in news:
            if channel is not None:
                await channel.send(new)

    @scrape_fitba.before_loop
    async def before_scrape_fitba(self):
        print('Scraper - Fit News: Waiting...')
        await self.bot.wait_until_ready()

    @tasks.loop(minutes=30)
    async def scrape_youtube(self):
        pass

def setup(bot):
    bot.add_cog(Scraper(bot))