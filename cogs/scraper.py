import discord
from discord.ext import commands
from discord.ext import tasks

import requests
import json
from bs4 import BeautifulSoup

from utils import notifications
from utils import misc
from utils import logger


class Scraper(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open(".\\config.json") as json_for_url:
            data = json.load(json_for_url)
        self.loginUrl = data["DLWMS"]["url"]

        self.send_notification.start()


    def get_value_for_input(self, html, inputName):
        return "" if html.find("input", {"name": inputName}) is None\
                  else html.find("input", {"name": inputName})["value"]

    def get_value_for_select(self, html, selectText):
        for option in html.select("#listInstitucija option"):
            if option.text == selectText:
                return str(option["value"])
        return ""

    def get_login(self):
        loginData = {}

        response = requests.get(self.loginUrl)
        response.raise_for_status()

        site = BeautifulSoup(response.text, "html.parser")
        
        hiddenInputArray = [
            "__LASTFOCUS", 
            "__EVENTTARGET", 
            "__EVENTARGUMENT", 
            "__VIEWSTATE", 
            "__VIEWSTATEGENERATOR", 
            "__EVENTVALIDATION"
        ]
        
        for hiddenInput in hiddenInputArray:
            loginData[hiddenInput] = self.get_value_for_input(site, hiddenInput)

        with open(".\\config.json") as json_data_file:
            data = json.load(json_data_file)
            
        #Login info
        loginData["txtBrojDosijea"] = data["DLWMS"]["userID"]
        loginData["txtLozinka"] = data["DLWMS"]["password"]
        loginData["listInstitucija"] = self.get_value_for_select(site, "Fakultet informacijskih tehnologija")

            
        #Submit button
        loginData["btnPrijava"] = self.get_value_for_input(site, "btnPrijava")
    

        return loginData

    def get_notifications(self):
        with requests.session() as session:
            try:
                loginResponse = session.post(self.loginUrl, data = self.get_login())
                response = BeautifulSoup(loginResponse.text, "html.parser")

                notificationsList = []
                news = response.select("ul.newslist")
                for new in news:
                    link = 'https://fit.ba/student/' + new.find("a", {"class": "linkButton"}).get("href")
                    title = new.find("a", {"class": "linkButton"}).text
                    date = new.find("span", {"id": "lblDatum"}).text[:16]
                    subject = new.find("span", {"id": "lblPredmet"}).text
                    author = new.find("a", {"id": "HyperLink9"}).text
                    content = new.find("div", {"class": "abstract"}).text

                    
                    notificationsList.append(
                        notifications.DLWMS_Notification(
                            link, title, date, subject, author, content
                        )
                    )
                                
                return notificationsList
            
            except Exception as err:
                print("Error: " + str(err))

    

    @tasks.loop(minutes = 1)
    async def send_notification(self):
        print("Scraping...")
        notificationsList = self.get_notifications()

        lastNotificationJson = {}
        
        with open(".\\lastNotification.json", "r") as jsonDataFile:
            lastNotificationJson = json.load(jsonDataFile)

        lastNotification = notifications.DLWMS_Notification(
            lastNotificationJson["link"],
            lastNotificationJson["title"],
            lastNotificationJson["date"],
            lastNotificationJson["subject"],
            lastNotificationJson["author"],
            lastNotificationJson["content"]
        )

        lastSent = lastNotification

        notificationsList.reverse()
        for notification in notificationsList or []:
            if notification > lastNotification:
                with open(".\\config.json") as jsonSubjectChannel:
                    data = json.load(jsonSubjectChannel)

                try:
                    channelName = data["DLWMS"]["subjects"][notification.subject]
                except:
                    channelName = "generalna-diskusija-3"
                    pass

                
                channel = self.client.get_channel(misc.getChannelID(self.client, channelName))
                if channel is not None:
                    await channel.send(embed = notification.getEmbed())
                lastSent = notification


        if lastSent != lastNotification:
            with open(".\\lastNotification.json", "w") as jsonDataFile:
                json.dump(lastSent.__dict__, jsonDataFile, indent = 4)


    def cog_unload(self):
        self.send_notification.cancel()

    @send_notification.before_loop
    async def before_send_notification(self):
        print('Scraper: Waiting...')
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Scraper(client))