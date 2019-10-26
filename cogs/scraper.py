import discord
from discord.ext import commands

import os
import sys


import requests
import json
from bs4 import BeautifulSoup

from utils.notifications import DLWMS_Notification
# from notifications import DLWMS_Notification


class Scraper(commands.Cog):
    def __init__(self, client):
        self.client = client

        with open("config.json") as json_for_url:
            data = json.load(json_for_url)
        self.loginUrl = data["DLWMS"]["url"]

        self.sendNotification()

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

        with open("config.json") as json_data_file:
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
                    mail = new.find("a", {"id": "HyperLink9"}).get("href")[7:]

                    
                    notificationsList.insert(0, DLWMS_Notification(link, title, date, subject, author, mail))
                
                return notificationsList.reverse()
            
            except:
                print("Error")

    def sendNotification(self):
        notificationsList = self.getNotifications()

        lastNotificationJson = {}
        
        with open("lastNotification.json", "r") as jsonDataFile:
            lastNotificationJson = json.load(jsonDataFile)

        lastNotification = DLWMS_Notification(
            lastNotificationJson["link"],
            lastNotificationJson["title"],
            lastNotificationJson["date"],
            lastNotificationJson["subject"],
            lastNotificationJson["author"],
            lastNotificationJson["mail"]
        )

                    
        for notification in notificationsList:
            if notification == lastNotification:
                break
            else:
                print(notification) ##send to discor
                with open("lastNotification.json", "w") as jsonDataFile:
                    json.dump(notification.__dict__, jsonDataFile, indent=4)

def setup(client):
    client.add_cog(Scraper(client))

# loginUrl = 'https://fit.ba/student/login.aspx'

# def getValueForInput(html, inputName):
#     return "" if html.find("input", {"name": inputName}) is None else html.find("input", {"name": inputName})["value"]

# def getValueForSelect(html, selectText):
#     for option in html.select("#listInstitucija option"):
#         if option.text == selectText:
#             return str(option["value"])
#     return ""

# def getLogin():
#     loginData = {}

#     response = requests.get(loginUrl)
#     response.raise_for_status()

#     site = BeautifulSoup(response.text, "html.parser")
    
#     hiddenInputArray = ["__LASTFOCUS", "__EVENTTARGET", "__EVENTARGUMENT", "__VIEWSTATE", "__VIEWSTATEGENERATOR", "__EVENTVALIDATION"]
#     for hiddenInput in hiddenInputArray:
#         loginData[hiddenInput] = getValueForInput(site, hiddenInput)

#     with open("config.json") as json_data_file:
#         data = json.load(json_data_file)
        
#     #Login info
#     loginData["txtBrojDosijea"] = data["DLWMS"]["userID"]
#     loginData["txtLozinka"] = data["DLWMS"]["password"]
#     loginData["listInstitucija"] = getValueForSelect(site, "Fakultet informacijskih tehnologija")

        
#     #Submit button
#     loginData["btnPrijava"] = getValueForInput(site, "btnPrijava")
    

#     return loginData

# def getNotifications():
#     with requests.session() as session:
#         try:
#             loginResponse = session.post(loginUrl, data=getLogin())
#             response = BeautifulSoup(loginResponse.text, "html.parser")

#             notifications = []
#             news = response.select("ul.newslist")
#             for new in news:
#                 link = 'https://fit.ba/student/' + new.find("a", {"class": "linkButton"}).get("href")
#                 title = new.find("a", {"class": "linkButton"}).text
#                 date = new.find("span", {"id": "lblDatum"}).text[:16]
#                 subject = new.find("span", {"id": "lblPredmet"}).text
#                 author = new.find("a", {"id": "HyperLink9"}).text
#                 mail = new.find("a", {"id": "HyperLink9"}).get("href")[7:]

                
#                 notifications.insert(0, DLWMS_Notification(link, title, date, subject, author, mail))
            
#             return notifications.reverse()
        
#         except:
#             print("Error")

# def sendNotification():
    
#     notifications = getNotifications()
# ##    for notification in notifications:
# ##        print(notification)

#     lastNotificationJson = {}
    
#     with open("lastNotification.json", "r") as jsonDataFile:
#         lastNotificationJson = json.load(jsonDataFile)

    
#     lastNotification = Notification(
#         lastNotificationJson["link"],
#         lastNotificationJson["title"],
#         lastNotificationJson["date"],
#         lastNotificationJson["subject"],
#         lastNotificationJson["author"],
#         lastNotificationJson["mail"]
#     )

                
#     for notification in notifications:
#         if notification == lastNotification:
#             break
#         else:
#             print(notification) ##send to discord
#             with open("lastNotification.json", "w") as jsonDataFile:
#                 json.dump(notification.__dict__, jsonDataFile, indent=4)
    

