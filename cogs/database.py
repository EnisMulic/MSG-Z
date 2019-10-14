import discord
from discord.ext import commands

import MySQLdb
import json


def getPassword():
    with open('.\\config.json') as json_data_file:
        data = json.load(json_data_file)
    return data["Database"]["Password"]


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.db = MySQLdb.connect(\
            host = "localhost", \
            user = "root", \
            passwd = getPassword(), \
            db = "FIT_Community", \
            charset = 'UTF8' \
        )

        self.cursor = self.db.cursor()
        self.setupDatabaseTables()

    def setupDatabaseTables(self):
        try:
            tableUsersQuery = "CREATE TABLE IF NOT EXISTS Users\
                (\
                    UserIndex NVARCHAR(8) NOT NULL PRIMARY KEY, \
                    Name NVARCHAR(32) NOT NULL, \
                    Username NVARCHAR(32) NOT NULL, \
                    Discriminator VARCHAR(4) NOT NULL, \
                    NumberOfPosts INT DEFAULT 0 \
                )"
            self.cursor.execute(tableUsersQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Roles: Something went wrong: " + str(err))
            pass

        try:
            tableRolesQuery = "CREATE TABLE IF NOT EXISTS Roles\
                (\
                    RoleID INT NOT NULL PRIMARY KEY, \
                    RoleName NVARCHAR(32) NOT NULL \
                )"
            self.cursor.execute(tableRolesQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Roles: Something went wrong: " + str(err))
            pass

        try:
            tableUsersRolesQuery = "CREATE TABLE IF NOT EXISTS UsersRoles\
                (\
                    UserIndex NVARCHAR(8) NOT NULL, \
                    RoleID INT NOT NULL, \
                    FOREIGN KEY (UserIndex) REFERENCES Users(UserIndex), \
                    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID), \
                    PRIMARY KEY (UserIndex, RoleID) \
                )"
            self.cursor.execute(tableUsersRolesQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Roles: Something went wrong: " + str(err))
            pass

        try:
            tablePostsQuery = "CREATE TABLE IF NOT EXISTS Posts\
                (\
                    PostID INT NOT NULL PRIMARY KEY, \
                    UserIndex NVARCHAR(8) NOT NULL, \
                    FOREIGN KEY (UserIndex) REFERENCES Users(UserIndex) \
                )"
            self.cursor.execute(tablePostsQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Roles: Something went wrong: " + str(err))
            pass


def setup(client):
    client.add_cog(Database(client))

