from datetime import datetime, date
import aiohttp
from bs4 import BeautifulSoup
import re

class FitBaScraper:
    def __init__(self):
        self.base_url = 'https://fit.ba'
        self.news_url = 'https://fit.ba/news'
        self.date = date.today()
        self.news = []

    async def fetch_data(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.news_url) as response:
                html = await response.text()
                response = BeautifulSoup(html, "html.parser")
                return response.select("li.media")

    async def parse_data(self):
        news = await self.fetch_data()

        for new in news[::-1]:
            link = self.base_url + new.find("a", {"class": "cover"}).get("href")
            meta = new.find("small").text
            date_str = re.search(r'\d{2}.\d{2}.\d{4}', meta).group()
            new_data = datetime.strptime(date_str, "%d.%m.%Y")
 
            if self.date == new_data.date() and link not in self.news:
                self.news.append(link)
                yield link


