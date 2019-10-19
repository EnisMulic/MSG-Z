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
        self.setup_database_tables()
     
    def setup_database_tables(self):
        try:
            tableUsersQuery = "CREATE TABLE IF NOT EXISTS Users\
                (\
                    UserIndex NVARCHAR(8) NOT NULL PRIMARY KEY, \
                    Name NVARCHAR(32) NOT NULL, \
                    Username NVARCHAR(32) NOT NULL, \
                    Discriminator VARCHAR(4) NOT NULL, \
                    StatusFakultet NVARCHAR(20), \
                    StatusDiscord NVARCHAR(20) NOT NULL, \
                    NumberOfPosts INT DEFAULT 0 \
                )"
            self.cursor.execute(tableUsersQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Users: Something went wrong: " + str(err))
            pass

        try:
            tableRolesQuery = "CREATE TABLE IF NOT EXISTS Roles\
                (\
                    RoleID BIGINT NOT NULL PRIMARY KEY, \
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
                    RoleID BIGINT NOT NULL, \
                    FOREIGN KEY (UserIndex) REFERENCES Users(UserIndex), \
                    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID), \
                    PRIMARY KEY (UserIndex, RoleID) \
                )"
            self.cursor.execute(tableUsersRolesQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table UsersRoles: Something went wrong: " + str(err))
            pass

        try:
            tablePostsQuery = "CREATE TABLE IF NOT EXISTS Posts\
                (\
                    PostID BIGINT NOT NULL PRIMARY KEY, \
                    ChannelID BIGINT NOT NULL, \
                    UserIndex NVARCHAR(8) NOT NULL, \
                    FOREIGN KEY (UserIndex) REFERENCES Users(UserIndex) \
                )"
            self.cursor.execute(tablePostsQuery)
        except MySQLdb.ProgrammingError as err:
            print("Table Posts: Something went wrong: " + str(err))
            pass
    
    @commands.command(aliases=["insert-role"])
    @commands.has_any_role('Administrator')   
    async def insert_role(self, ctx, role: discord.Role):
        try:
            InsertRoleQuery = 'INSERT INTO Roles(RoleID, RoleName) \
                               VALUES({}, "{}");'.format(
                                   role.id, 
                                   role.name
                                )
            self.cursor.execute(InsertRoleQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Insert Role: Something went wrong: " + str(err))
            pass
        pass

    async def insert_member(self, ctx, member: discord.Member, userIndex):
        try:
            insertMemberQuery = 'INSERT INTO Users(\
                                    UserIndex, \
                                    Name,\
                                    Username, \
                                    Discriminator, \
                                    StatusFakultet, \
                                    StatusDiscord\
                                )\
                                VALUES(\
                                    "{}",\
                                    "{}",\
                                    "{}",\
                                    "{}",\
                                    "{}"\
                                );'.format(
                                    userIndex, 
                                    member.nick, 
                                    member.name, 
                                    member.discriminator,
                                    "Aktivan", 
                                    "Aktivan"
                                )

            self.cursor.execute(insertMemberQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Insert Member: Something went wrong: " + str(err))
            pass
        pass

    async def change_member_index(self, ctx, member: discord.Member, userIndex):
        try:
            changeMemberIndexQuery = 'UPDATE Users\
                                      SET UserIndex = "{}"\
                                      WHERE Username = "{}" AND\
                                            Discriminator = "{}"'.format(
                                                userIndex,
                                                member.name,
                                                member.discriminator
                                            )
            
            self.cursor.execute(changeMemberIndexQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Index: Something went wrong: " + str(err))
            pass
        pass    

    async def change_member_fakultet_status(self, ctx, member: discord.Member, status):
        try:
            changeMemberFakultetStatusQuery = 'UPDATE Users\
                                               SET StatusFakultet = "{}"\
                                               WHERE Username = "{}" AND\
                                               Discriminator = "{}"'.format(
                                                   status,
                                                   member.name,
                                                   member.discriminator
                                               )
            
            self.cursor.execute(changeMemberFakultetStatusQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Fakultet Status: Something went wrong: " + str(err))
            pass
        pass

    async def change_member_discord_status(self, ctx, member: discord.Member, status):
        try:
            changeMemberDiscordStatusQuery = 'UPDATE Users\
                                              SET StatusDiscord = "{}"\
                                              WHERE Username = "{}" AND\
                                              Discriminator = "{}"'.format(
                                                  status,
                                                  member.name,
                                                  member.discriminator
                                              )
            
            self.cursor.execute(changeMemberDiscordStatusQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Discord Status: Something went wrong: " + str(err))
            pass
        pass

        # Change users in-server nickname
    async def change_member_name(self, ctx, member: discord.Member, name):
        try:
            changeMemberNameQuery = 'UPDATE Users\
                                     SET Name = "{}"\
                                     WHERE Username = "{}" AND\
                                           Discriminator = "{}"'.format(
                                                name, 
                                                member.name,
                                                member.discriminator
                                            ) 
            
            self.cursor.execute(changeMemberNameQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Name: Something went wrong: " + str(err))
            pass
        pass

    async def change_member_username(self, before: discord.Member, after: discord.Member):
        try:
            changeMemberUsernameQuery = 'UPDATE Users\
                                         SET Username = "{}"\
                                         WHERE Username = "{}" AND\
                                               Discriminator = "{}";'.format(
                                                   after.nick,
                                                   before.nick,
                                                   before.discriminator
                                               )
            
            self.cursor.execute(changeMemberUsernameQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Username: Something went wrong: " + str(err))
            pass
        pass

    #probably works?
    async def change_member_discriminator(self, before: discord.Member, after: discord.Member):
        try:
            changeMemberDiscriminatorQuery = 'UPDATE Users\
                                              SET Discriminator = "{}"\
                                              WHERE Username = "{}" AND\
                                                    Discriminator = "{}";'.format(
                                                        after.discriminator,
                                                        before.nick,
                                                        before.discriminator
                                                    )
            
            self.cursor.execute(changeMemberDiscriminatorQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Change Member Disciminator: Something went wrong: " + str(err))
            pass
        pass

    async def insert_post(self, ctx, channelID, messageID):
        try:
            getUserIndexQuery = 'SELECT * \
                                 FROM Users \
                                 WHERE Username = "{}" AND \
                                       Discriminator = "{}";'.format(
                                           ctx.author.name, 
                                           ctx.author.discriminator
                                        )

            userIndex = self.cursor.execute(getUserIndexQuery)


            InsertPostQuery = 'INSERT INTO Posts(PostID, ChannelID, UserIndex) \
                               VALUES({}, {}, "{}");'.format(
                                   messageID, 
                                   channelID, 
                                   userIndex
                                )

            self.cursor.execute(InsertPostQuery)
            self.db.commit()
        except MySQLdb.ProgrammingError as err:
            print("Procedure Insert Post: Somethin went wrong: " + str(err))
            pass
        pass

    

    

def setup(client):
    client.add_cog(Database(client))

