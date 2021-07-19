import aiohttp
import os
from bs4 import BeautifulSoup


class DLWMSScraper:
    def __init__(self):
        self.base_url = os.environ.get("DLWMS_BASE_URL")
        self.login_url = os.environ.get("DLWMS_LOGIN_URL")
        self.accounts = []

        dlwms_username_1 = os.environ.get("DLWMS_USERNAME_1")
        dlwms_password_1 = os.environ.get("DLWMS_PASSWORD_1")

        self.accounts.append({
            "username": dlwms_username_1,
            "password": dlwms_password_1
        })

        dlwms_username_2 = os.environ.get("DLWMS_USERNAME_2")
        dlwms_password_2 = os.environ.get("DLWMS_PASSWORD_2")

        self.accounts.append({
            "username": dlwms_username_2,
            "password": dlwms_password_2
        })

    def _get_value_for_input(self, html, inputName):
        return "" if html.find("input", {"name": inputName}) is None\
            else html.find("input", {"name": inputName})["value"]

    def _get_value_for_select(self, html, selectText):
        for option in html.select("#listInstitucija option"):
            if option.text == selectText:
                return str(option["value"])
        return ""

    def build_login_form_data(self, html):
        login_form = {}

        html = BeautifulSoup(html, "html.parser")

        hidden_input_array = [
            "__LASTFOCUS",
            "__EVENTTARGET",
            "__EVENTARGUMENT",
            "__VIEWSTATE",
            "__VIEWSTATEGENERATOR",
            "__EVENTVALIDATION"
        ]

        for hidden_input in hidden_input_array:
            login_form[hidden_input] = self._get_value_for_input(html, hidden_input)

        login_form["listInstitucija"] = self._get_value_for_select(html, "Fakultet informacijskih tehnologija")

        # Submit button
        login_form["btnPrijava"] = self._get_value_for_input(html, "btnPrijava")

        return login_form

    def add_auth_to_login_form(self, login_form, username, password):
        login_form["txtBrojDosijea"] = username
        login_form["txtLozinka"] = password

        return login_form

    async def fetch(self, url):
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            html = await response.text()
            return html

    async def fetch_with_login(self, url, data):
        async with aiohttp.ClientSession() as session:
            response = await session.post(url, data = data)
            html = await response.text()
            return html

    async def parse_data(self):
        html = await self.fetch(self.base_url)
        login_form = self.build_login_form_data(html)

        for account in self.accounts:
            login_form = self.add_auth_to_login_form(login_form, account["username"], account["password"])

            html = await self.fetch_with_login(self.login_url, login_form)
            html = BeautifulSoup(html, "html.parser")

            news = html.select("ul.newslist")
            for new in news:
                url = self.base_url + new.find("a", {"class": "linkButton"}).get("href")
                title = new.find("a", {"class": "linkButton"}).text
                subject = new.find("span", {"id": "lblPredmet"}).text
                author = new.find("a", {"id": "HyperLink9"}).text
                content = new.find("div", {"class": "abstract"}).text
                date = new.find("span", {"id": "lblDatum"}).text[:16]

                if content.isspace():
                    content = "N/A"

                yield {
                    "url": url,
                    "date": date,
                    "title": title,
                    "author": author,
                    "content": content,
                    "subject": subject
                }
