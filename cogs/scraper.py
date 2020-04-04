import discord
from discord.ext import commands
from discord.ext import tasks


import requests
import json
from bs4 import BeautifulSoup

import sqlalchemy.orm.query
from sqlalchemy.exc import SQLAlchemyError


from models.user import User

from utils import notifications
from utils import misc
from utils import logger


class Scraper(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open('.\\config.json', "r", encoding="utf-8") as json_for_url:
            data = json.load(json_for_url)
        self.loginUrl = data["DLWMS"]["url"]

        self.get_notifications()


    def get_value_for_input(self, html, inputName):
        return "" if html.find("input", {"name": inputName}) is None\
                  else html.find("input", {"name": inputName})["value"]

    def get_value_for_select(self, html, selectText):
        for option in html.select("#listInstitucija option"):
            if option.text == selectText:
                return str(option["value"])
        return ""

    def get_login(self):
        login_data = {}

        response = requests.get(self.loginUrl)
        response.raise_for_status()

        site = BeautifulSoup(response.text, "html.parser")
        
        hidden_input_array = [
            "__LASTFOCUS", 
            "__EVENTTARGET", 
            "__EVENTARGUMENT", 
            "__VIEWSTATE", 
            "__VIEWSTATEGENERATOR", 
            "__EVENTVALIDATION"
        ]
        
        for hidden_input in hidden_input_array:
            login_data[hidden_input] = self.get_value_for_input(site, hidden_input)

        with open(".\\config.json", "r", encoding="utf-8") as json_data_file:
            data = json.load(json_data_file)
            
        #Login info
        login_data["txtBrojDosijea"] = data["DLWMS"]["userID"]
        login_data["txtLozinka"] = data["DLWMS"]["password"]
        login_data["listInstitucija"] = self.get_value_for_select(site, "Fakultet informacijskih tehnologija")

            
        #Submit button
        login_data["btnPrijava"] = self.get_value_for_input(site, "btnPrijava")
    

        return login_data

    @tasks.loop(minutes = 1)
    async def send_notifications(self, session, login_response):
        try:
            print("Scraping...")
            
            content_response = session.get('https://fit.ba/student/', cookies = login_response.cookies)
            response = BeautifulSoup(content_response.text, "html.parser")

            notifications_list = []
            news = response.select("ul.newslist")
            for new in news:
                link = 'https://fit.ba/student/' + new.find("a", {"class": "linkButton"}).get("href")
                title = new.find("a", {"class": "linkButton"}).text
                date = new.find("span", {"id": "lblDatum"}).text[:16]
                subject = new.find("span", {"id": "lblPredmet"}).text
                author = new.find("a", {"id": "HyperLink9"}).text
                content = new.find("div", {"class": "abstract"}).text
                
                if content.isspace(): content = "N/A"
                    
                notifications_list.append(
                    notifications.DLWMS_Notification(
                        link, title, date, subject, author, content
                    )
                )

            
            last_notification_json = {}
        
            with open(".\\last_notification.json", "r", encoding="utf-8") as jsonDataFile:
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
                    with open(".\\config.json", "r", encoding="utf-8") as jsonSubjectChannel:
                        data = json.load(jsonSubjectChannel)

                    try:  
                        notification.subject = notification.subject.translate({ord(i): None for i in '*'})
                        channelName = data["DLWMS"]["subjects"][notification.subject]
                    except:
                        channelName = "obavijesti"
                        
                        
                    channel = self.client.get_channel(misc.getChannelID(self.client, channelName))
                    if channel is not None:
                        await channel.send(embed = notification.getEmbed())
                    lastSent = notification


            if lastSent != last_notification:
                with open(".\\last_notification.json", "w", encoding="utf-8") as jsonDataFile:
                    json.dump(lastSent.__dict__, jsonDataFile, indent = 4)
            
        except Exception as err:
            print("Error: " + str(err))        
            

    

    
    def get_notifications(self):
        try:
            with requests.session() as session:
                login_response = session.post(self.loginUrl, data = self.get_login())
            self.send_notifications.start(session, login_response)
        
        except Exception as err:
            print(str(err))
            self.get_notifications()
        
            


    def cog_unload(self):
        self.send_notifications.cancel()
        

    @send_notifications.before_loop
    async def before_send_notifications(self):
        print('Scraper: Waiting...')
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(Scraper(client))