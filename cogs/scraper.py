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

        

    def getValueForInput(self, html, inputName):
        return "" if html.find("input", {"name": inputName}) is None\
                  else html.find("input", {"name": inputName})["value"]

    def getValueForSelect(self, html, selectText):
        for option in html.select("#listInstitucija option"):
            if option.text == selectText:
                return str(option["value"])
        return ""

    def getLogin(self):
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
            loginData[hiddenInput] = self.getValueForInput(site, hiddenInput)

        with open(".\\config.json") as json_data_file:
            data = json.load(json_data_file)
            
        #Login info
        loginData["txtBrojDosijea"] = data["DLWMS"]["userID"]
        loginData["txtLozinka"] = data["DLWMS"]["password"]
        loginData["listInstitucija"] = self.getValueForSelect(site, "Fakultet informacijskih tehnologija")

            
        #Submit button
        loginData["btnPrijava"] = self.getValueForInput(site, "btnPrijava")
    

        return loginData

    def getNotifications(self):
        with requests.session() as session:
            try:
                loginResponse = session.post(self.loginUrl, data = self.getLogin())
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
                
                # notificationsList.reverse()
                
                return notificationsList
            
            except Exception as err:
                print("Error: " + str(err))

    
    # @commands.command()
    # @commands.has_any_role('Administrator')
    @tasks.loop(minutes = 1)
    async def sendNotification(self):
        print("Sending...")
        notificationsList = self.getNotifications()

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

        # for notification in notificationsList:
        #     if notification > lastNotification:
        #         print(notification)

        
        for notification in notificationsList or []:
            print(notification)
            if notification == lastNotification:
                break;
            else:
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


        with open(".\\lastNotification.json", "w") as jsonDataFile:
            json.dump(notificationsList[0].__dict__, jsonDataFile, indent = 4)

def setup(client):
    client.add_cog(Scraper(client))