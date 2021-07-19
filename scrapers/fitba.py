import aiohttp
from bs4 import BeautifulSoup
import re
import os


class FitBaScraper:
    def __init__(self):
        self.base_url = os.environ.get("FITBA_BASE_URL")
        self.news_url = os.environ.get("FITBA_NEWS_URL")

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.news_url) as response:
                html = await response.text()
                response = BeautifulSoup(html, "html.parser")
                return response.select("li.media")

    async def parse_data(self):
        news = await self.fetch_data()

        for new in news:
            url = self.base_url + new.find("a", {"class": "cover"}).get("href")
            meta = new.find("small").text
            date = re.search(r'\d{2}.\d{2}.\d{4}', meta).group()

            yield {
                "url": url,
                "date": date
            }
